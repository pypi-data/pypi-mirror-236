from transformers import AutoModel, AutoTokenizer
import time
import threading
import importlib
from void_terminal.toolbox import update_ui, get_conf, Singleton
from multiprocessing import Process, Pipe

def SingletonLocalLLM(cls):
    """
    Single instance decorator
    """
    _instance = {}
    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
            return _instance[cls]
        elif _instance[cls].corrupted:
            _instance[cls] = cls(*args, **kargs)
            return _instance[cls]
        else:
            return _instance[cls]
    return _singleton

class LocalLLMHandle(Process):
    def __init__(self):
        # ⭐Main process execution
        super().__init__(daemon=True)
        self.corrupted = False
        self.load_model_info()
        self.parent, self.child = Pipe()
        self.running = True
        self._model = None
        self._tokenizer = None
        self.info = ""
        self.check_dependency()
        self.start()
        self.threadLock = threading.Lock()

    def load_model_info(self):
        # 🏃‍♂️🏃‍♂️🏃‍♂️ Subprocess execution
        raise NotImplementedError("Method not implemented yet")
        self.model_name = ""
        self.cmd_to_install = ""

    def load_model_and_tokenizer(self):
        """
        This function should return the model and the tokenizer
        """
        # 🏃‍♂️🏃‍♂️🏃‍♂️ Subprocess execution
        raise NotImplementedError("Method not implemented yet")

    def llm_stream_generator(self, **kwargs):
        # 🏃‍♂️🏃‍♂️🏃‍♂️ Subprocess execution
        raise NotImplementedError("Method not implemented yet")
        
    def try_to_import_special_deps(self, **kwargs):
        """
        import something that will raise error if the user does not install requirement_*.txt
        """
        # ⭐Main process execution
        raise NotImplementedError("Method not implemented yet")

    def check_dependency(self):
        # ⭐Main process execution
        try:
            self.try_to_import_special_deps()
            self.info = "Dependency check passed"
            self.running = True
        except:
            self.info = f"Missing{self.model_name}Dependencies of，If you want to use{self.model_name}，In addition to the basic pip dependencies，You also need to run{self.cmd_to_install}Installation{self.model_name}Dependencies of。"
            self.running = False

    def run(self):
        # 🏃‍♂️🏃‍♂️🏃‍♂️ Subprocess execution
        # First run，Load parameters
        try:
            self._model, self._tokenizer = self.load_model_and_tokenizer()
        except:
            self.running = False
            from void_terminal.toolbox import trimmed_format_exc
            self.child.send(f'[Local Message] Cannot load properly{self.model_name}Parameters of.' + '\n```\n' + trimmed_format_exc() + '\n```\n')
            self.child.send('[FinishBad]')
            raise RuntimeError(f"Cannot load properly{self.model_name}parameters!")

        while True:
            # Enter task waiting state
            kwargs = self.child.recv()
            # Received message，Start requesting
            try:
                for response_full in self.llm_stream_generator(**kwargs):
                    self.child.send(response_full)
                self.child.send('[Finish]')
                # Request processing ends，Start the next loop
            except:
                from void_terminal.toolbox import trimmed_format_exc
                self.child.send(f'[Local Message] Call{self.model_name}Failure.' + '\n```\n' + trimmed_format_exc() + '\n```\n')
                self.child.send('[Finish]')

    def stream_chat(self, **kwargs):
        # ⭐Main process execution
        self.threadLock.acquire()
        self.parent.send(kwargs)
        while True:
            res = self.parent.recv()
            if res == '[Finish]': 
                break
            if res == '[FinishBad]': 
                self.running = False
                self.corrupted = True
                break
            else: 
                yield res
        self.threadLock.release()
    


def get_local_llm_predict_fns(LLMSingletonClass, model_name):
    load_message = f"{model_name}Not loaded yet，Loading takes some time。Attention，Depending on`config.py`Configuration，{model_name}Consumes a large amount of memory（CPU）Or video memory（GPU），May cause low-end computers to freeze..."

    def predict_no_ui_long_connection(inputs, llm_kwargs, history=[], sys_prompt="", observe_window=[], console_slience=False):
        """
            ⭐Multi-threaded method
            For function details, please see request_llm/bridge_all.py
        """
        _llm_handle = LLMSingletonClass()
        if len(observe_window) >= 1: observe_window[0] = load_message + "\n\n" + _llm_handle.info
        if not _llm_handle.running: raise RuntimeError(_llm_handle.info)

        # ChatGLM has no sys_prompt interface，Therefore, add prompt to history
        history_feedin = []
        history_feedin.append([sys_prompt, "Certainly!"])
        for i in range(len(history)//2):
            history_feedin.append([history[2*i], history[2*i+1]] )

        watch_dog_patience = 5 # Watchdog (watchdog) Patience, Set 5 seconds
        response = ""
        for response in _llm_handle.stream_chat(query=inputs, history=history_feedin, max_length=llm_kwargs['max_length'], top_p=llm_kwargs['top_p'], temperature=llm_kwargs['temperature']):
            if len(observe_window) >= 1:
                observe_window[0] = response
            if len(observe_window) >= 2:  
                if (time.time()-observe_window[1]) > watch_dog_patience: raise RuntimeError("Program terminated。")
        return response



    def predict(inputs, llm_kwargs, plugin_kwargs, chatbot, history=[], system_prompt='', stream = True, additional_fn=None):
        """
            ⭐Single-threaded method
            For function details, please see request_llm/bridge_all.py
        """
        chatbot.append((inputs, ""))

        _llm_handle = LLMSingletonClass()
        chatbot[-1] = (inputs, load_message + "\n\n" + _llm_handle.info)
        yield from update_ui(chatbot=chatbot, history=[])
        if not _llm_handle.running: raise RuntimeError(_llm_handle.info)

        if additional_fn is not None:
            from void_terminal.core_functional import handle_core_functionality
            inputs, history = handle_core_functionality(additional_fn, inputs, history, chatbot)

        # Process historical information
        history_feedin = []
        history_feedin.append([system_prompt, "Certainly!"])
        for i in range(len(history)//2):
            history_feedin.append([history[2*i], history[2*i+1]] )

        # Start receiving replies
        response = f"[Local Message]: Waiting{model_name}Responding ..."
        for response in _llm_handle.stream_chat(query=inputs, history=history_feedin, max_length=llm_kwargs['max_length'], top_p=llm_kwargs['top_p'], temperature=llm_kwargs['temperature']):
            chatbot[-1] = (inputs, response)
            yield from update_ui(chatbot=chatbot, history=history)

        # Summary output
        if response == f"[Local Message]: Waiting{model_name}Responding ...":
            response = f"[Local Message]: {model_name}Response exception ..."
        history.extend([inputs, response])
        yield from update_ui(chatbot=chatbot, history=history)

    return predict_no_ui_long_connection, predict