import os 
from tpf.box.fil import log as log2 

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
log_file = "main.log"
log_file = os.path.join(BASE_DIR,log_file)

def log(msg):
    log2(msg, log_file=log_file) 
    
log("slowly ...")