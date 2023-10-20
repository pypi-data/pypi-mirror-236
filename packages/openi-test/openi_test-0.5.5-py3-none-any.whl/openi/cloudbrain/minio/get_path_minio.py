import os
def get_code_path_minio():
    """
    获取源代码存储在minio,挂载到镜像后的代码路径
    """
    code_path = os.getenv("CODE_PATH")
    if code_path is None:
    	raise ValueError("Failed to get the environment variable, please ensure that the CODE_PATH environment variable has been set.")
    return code_path 

def get_dataset_path_minio(
    dataset_name: str,
):
    """
    获取源数据集存储在minio,挂载到镜像后的数据集路径
    """
    dataset_path = os.getenv("DATASET_PATH")
    if dataset_path is None:
    	raise ValueError("环境变量获取失败，请确保设置了DATASET_PATH环境变量。")
    if dataset_name != "":
        return os.path.join(dataset_path, dataset_name)
    return dataset_path 

def get_pretrain_model_path_minio(
    pretrain_model_name: str,
):
    """
    获取源预训练模型存储在minio,挂载到镜像后的预训练模型路径
    """
    pretrain_model_path = os.getenv("PRETRAIN_MODEL_PATH")
    if pretrain_model_path is None:
    	raise ValueError("环境变量获取失败，请确保设置了PRETRAIN_MODEL_PATH环境变量。")
    if pretrain_model_name != "":
        return os.path.join(pretrain_model_path, pretrain_model_name)
    return pretrain_model_path 
    
def get_output_path_minio():
    """
    获取需要存储在minio的输出路径
    """    
    output_path = os.getenv("OUTPUT_PATH")
    if output_path is None:
    	raise ValueError("环境变量获取失败，请确保设置了OUTPUT_PATH环境变量。")
    return output_path

def download_code_minio():
    code_path = os.getenv("CODE_PATH")
    if code_path is None:
    		raise ValueError("环境变量获取失败，请确保设置了CODE_PATH环境变量。")
    return f"代码处理结束，容器内代码存储在{code_path}" 

def download_dataset_minio():
    dataset_path = os.getenv("DATASET_PATH")
    if dataset_path is None:
    		raise ValueError("环境变量获取失败，请确保设置了DATASET_PATH环境变量。")
    return f"数据集处理结束，容器内数据集存储在{dataset_path}"
    
def download_pretrain_model_minio():
    pretrain_model_path = os.getenv("PRETRAIN_MODEL_PATH")
    if pretrain_model_path is None:
    		raise ValueError("环境变量获取失败，请确保设置了PRETRAIN_MODEL_PATH环境变量。")
    return f"预训练模型处理结束，容器内预训练模型存储在{pretrain_model_path}"    

def upload_output_minio():
    output_path = os.getenv("OUTPUT_PATH")
    if output_path is None:
    		raise ValueError("环境变量设置失败，请确保设置了OUTPUT_PATH环境变量。")
    return f"回传{output_path}路径下的结果文件"      