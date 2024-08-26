# import the libraries
import os
from pypdf import PdfReader
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError
import logging

load_dotenv()

######################################################
######  PDF TO TEXT
######################################################

def pdf_to_text_01(my_pdf_file):
    """
    function accepting a pdf file as input and returning a text as output
    """
    text = ""
    try:
        reader = PdfReader(my_pdf_file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    except:
        pass
    finally:
        return text
    
######################################################
######  CREATE A FOLDER IN S3
######################################################

def tfm_create_folder(Key,Bucket):
    """Crea una carpeta en un bucket de S3"""
    
    AWS_S3_CREDS = {
        "aws_access_key_id": os.getenv("S3_ACCESS_KEY"),
        "aws_secret_access_key": os.getenv("S3_SECRET_KEY"),
    }
    # Configuración de las credenciales de AWS
    s3_client = boto3.client('s3', **AWS_S3_CREDS)
    
    try:
        # Asegúrate de que la clave termine en '/'
        folder_key = Key if Key.endswith('/') else Key + '/'
        
        s3_client.put_object(
            Bucket=Bucket, 
            Key=folder_key
        )
        logging.info(f"Carpeta '{Key}' creada exitosamente en el bucket '{Bucket}'.")
        return True
    except ClientError as e:
        logging.error(f"Error al crear la carpeta '{Key}': {e}")
        return False

######################################################
######  DELETE A FOLDER FROM S3
######################################################

def tfm_delete_folder(bucket,folder_name):
    """Borra una carpeta y todo su contenido en un bucket de S3"""
    
    AWS_S3_CREDS = {
        "aws_access_key_id": os.getenv("S3_ACCESS_KEY"),
        "aws_secret_access_key": os.getenv("S3_SECRET_KEY"),
    }
    
    s3_client = boto3.client('s3', region_name=os.getenv('AWS_DEFAULT_REGION'), **AWS_S3_CREDS)
    
    try:
        folder_key = folder_name if folder_name.endswith('/') else folder_name + '/'
        objects_to_delete = s3_client.list_objects_v2(Bucket=bucket, Prefix=folder_key)

        if 'Contents' in objects_to_delete:
            delete_keys = [{'Key': obj['Key']} for obj in objects_to_delete['Contents']]
            s3_client.delete_objects(Bucket=bucket, Delete={'Objects': delete_keys})
            logging.info(f"Carpeta '{folder_name}' y su contenido han sido eliminados del bucket '{bucket}'.")
        else:
            logging.info(f"La carpeta '{folder_name}' está vacía o no existe.")
            return False

        return True
    except ClientError as e:
        logging.error(f"Error al borrar la carpeta '{folder_name}': {e}")
        return False

######################################################
######  UPLOAD ALL THE PDF FROM S3
######################################################

def tfm_upload_file(file_name, bucket, object_name=None):
    """Sube un archivo a un bucket de S3"""
    if object_name is None:
        object_name = os.path.basename(file_name)

    s3_client = boto3.client('s3', region_name=os.getenv('AWS_DEFAULT_REGION'))
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

######################################################
######  DOWNLOAD ONE FILE FROM S3
######################################################

def tfm_download_one_file_from_s3(filename):

    AWS_S3_CREDS = {
        "aws_access_key_id":os.getenv("S3_ACCESS_KEY"),
        "aws_secret_access_key":os.getenv("S3_SECRET_KEY")
    }

    # get the credentials 
    s3_client = boto3.client('s3', **AWS_S3_CREDS)

    # bucket name
    bucket_name = os.getenv("S3_BUCKET_NAME")

    # display list of files
    list_files=s3_client.list_objects_v2(Bucket=bucket_name)["Contents"]

    # mostrar los archivos
    for files in list_files:
        if files["Key"].startswith("231033630"):
            # if the filename = actual file
            
            if files["Key"]==filename:

                # create files
                path=os.path.join(os.getcwd(),"./api/data",files["Key"])
                # download files
                s3_client.download_file(
                        Bucket=bucket_name,
                        Key=files["Key"],
                        Filename=path
                    )

######################################################
######  DOWNLOAD ALL FILES FROM S3
######################################################

def tfm_download_all_files_from_s3():

    AWS_S3_CREDS = {
        "aws_access_key_id":os.getenv("S3_ACCESS_KEY"),
        "aws_secret_access_key":os.getenv("S3_SECRET_KEY")
    }

    # get the credentials 
    s3_client = boto3.client('s3', **AWS_S3_CREDS)

    # bucket name
    bucket_name = os.getenv("S3_BUCKET_NAME")

    # display list of files
    list_files=s3_client.list_objects_v2(Bucket=bucket_name)["Contents"]

    # create a tuple to store the files uploaded
    files_uploaded=[]

    # mostrar los archivos
    for files in list_files:
        if files["Key"].startswith("231033630"):
            # create files
            path=os.path.join(os.getcwd(),"./api/data",files["Key"])
            # download files
            s3_client.download_file(
                    Bucket=bucket_name,
                    Key=files["Key"],
                    Filename=path
                )
            files_uploaded.append(files["Key"])

    return files_uploaded

if __name__ == '__main__':
    pass
