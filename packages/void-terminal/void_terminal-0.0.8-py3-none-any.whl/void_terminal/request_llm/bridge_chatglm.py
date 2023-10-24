
from transformers import AutoModel, AutoTokenizer
import time
import threading
import importlib
from void_terminal.toolbox import update_ui, get_conf, ProxyNetworkActivate
from multiprocessing import Process, Pipe

load_message = "ChatGLM has not been loaded，Loading takes some time。Attention，Depending on`config.py`Configuration，ChatGLM consumes a lot of memory（CPU）Or video memory（GPU），May cause low-end computers to freeze..."

#################################################################################
class GetGLMHandle(Process):
    def __init__(self):
        super().__init__(daemon=True)
        self.parent, self.child = Pipe()
        self.chatglm_model = None
        self.chatglm_tokenizer = None
        self.info = ""
        self.success = True
        self.check_dependency()
        self.start()
        self.threadLock = threading.Lock()
        
    def check_dependency(self):
        try:
            import sentencepiece
            self.info = "Dependency check passed"
            self.success = True
        except:
            self.info = "Missing dependency for ChatGLM，If you want to use ChatGLM，In addition to the basic pip dependencies，You also need to run`pip install -r request_llm/requirements_chatglm.txt`Install dependencies for ChatGLM。"
            self.success = False

    def ready(self):
        return self.chatglm_model is not None

    def run(self):
        # Subprocess execution
        # First run，Load parameters
        retry = 0
        LOCAL_MODEL_QUANT, device = get_conf('LOCAL_MODEL_QUANT', 'LOCAL_MODEL_DEVICE')

        if LOCAL_MODEL_QUANT == "INT4":         # INT4
            _model_name_ = "THUDM/chatglm2-6b-int4"
        elif LOCAL_MODEL_QUANT == "INT8":       # INT8
            _model_name_ = "THUDM/chatglm2-6b-int8"
        else:
            _model_name_ = "THUDM/chatglm2-6b"  # FP16

        while True:
            try:
                with ProxyNetworkActivate('Download_LLM'):
                    if self.chatglm_model is None:
                        self.chatglm_tokenizer = AutoTokenizer.from_pretrained(_model_name_, trust_remote_code=True)
                        if device=='cpu':
                            self.chatglm_model = AutoModel.from_pretrained(_model_name_, trust_remote_code=True).float()
                        else:
                            self.chatglm_model = AutoModel.from_pretrained(_model_name_, trust_remote_code=True).half().cuda()
                        self.chatglm_model = self.chatglm_model.eval()
                        break
                    else:
                        break
            except:
                retry += 1
                if retry > 3: 
                    self.child.send('[Local Message] Call ChatGLM fail, unable to load parameters for ChatGLM。')
                    raise RuntimeError("Unable to load parameters for ChatGLM!")

        while True:
            # Enter task waiting state
            kwargs = self.child.recv()
            # Received message，Start requesting
            try:
                for response, history in self.chatglm_model.stream_chat(self.chatglm_tokenizer, **kwargs):
                    self.child.send(response)
                    # # Receive possible termination command in the middle（If any）
                    # if self.child.poll(): 
                    #     command = self.child.recv()
                    #     if command == '[Terminate]': break
            except:
                from void_terminal.toolbox import trimmed_format_exc
                self.child.send('[Local Message] Call ChatGLM fail.' + '\n```\n' + trimmed_format_exc() + '\n```\n')
            # Request processing ends，Start the next loop
            self.child.send('[Finish]')

    def stream_chat(self, **kwargs):
        # Main process execution
        self.threadLock.acquire()
        self.parent.send(kwargs)
        while True:
            res = self.parent.recv()
            if res != '[Finish]':
                yield res
            else:
                break
        self.threadLock.release()
    
global glm_handle
glm_handle = None
#################################################################################
def predict_no_ui_long_connection(inputs, llm_kwargs, history=[], sys_prompt="", observe_window=[], console_slience=False):
    """
        Multithreading method
        For function details, please see request_llm/bridge_all.py
    """
    global glm_handle
    if glm_handle is None:
        glm_handle = GetGLMHandle()
        if len(observe_window) >= 1: observe_window[0] = load_message + "\n\n" + glm_handle.info
        if not glm_handle.success: 
            error = glm_handle.info
            glm_handle = None
            raise RuntimeError(error)

    # ChatGLM has no sys_prompt interface，Therefore, add prompt to history
    history_feedin = []
    history_feedin.append(["What can I do?", sys_prompt])
    for i in range(len(history)//2):
        history_feedin.append([history[2*i], history[2*i+1]] )

    watch_dog_patience = 5 # Watchdog (watchdog) Patience, Set 5 seconds
    response = ""
    for response in glm_handle.stream_chat(query=inputs, history=history_feedin, max_length=llm_kwargs['max_length'], top_p=llm_kwargs['top_p'], temperature=llm_kwargs['temperature']):
        if len(observe_window) >= 1:  observe_window[0] = response
        if len(observe_window) >= 2:  
            if (time.time()-observe_window[1]) > watch_dog_patience:
                raise RuntimeError("Program terminated。")
    return response



def predict(inputs, llm_kwargs, plugin_kwargs, chatbot, history=[], system_prompt='', stream = True, additional_fn=None):
    """
        Single-threaded method
        For function details, please see request_llm/bridge_all.py
    """
    chatbot.append((inputs, ""))

    global glm_handle
    if glm_handle is None:
        glm_handle = GetGLMHandle()
        chatbot[-1] = (inputs, load_message + "\n\n" + glm_handle.info)
        yield from update_ui(chatbot=chatbot, history=[])
        if not glm_handle.success: 
            glm_handle = None
            return

    if additional_fn is not None:
        from void_terminal.core_functional import handle_core_functionality
        inputs, history = handle_core_functionality(additional_fn, inputs, history, chatbot)

    # Process historical information
    history_feedin = []
    history_feedin.append(["What can I do?", system_prompt] )
    for i in range(len(history)//2):
        history_feedin.append([history[2*i], history[2*i+1]] )

    # Start receiving replies from ChatGLM
    response = "[Local Message]: Waiting for response from ChatGLM ..."
    for response in glm_handle.stream_chat(query=inputs, history=history_feedin, max_length=llm_kwargs['max_length'], top_p=llm_kwargs['top_p'], temperature=llm_kwargs['temperature']):
        chatbot[-1] = (inputs, response)
        yield from update_ui(chatbot=chatbot, history=history)

    # Summary output
    if response == "[Local Message]: Waiting for response from ChatGLM ...":
        response = "[Local Message]: ChatGLM response exception ..."
    history.extend([inputs, response])
    yield from update_ui(chatbot=chatbot, history=history)
