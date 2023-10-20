version = 0.1



import subprocess

def get_images(image_name):
    subprocess.run(["docker pull", image_name])
    return True


def run_container(name, ports, image):
    subprocess.run(["docker run -it -d --name", name,"-p", ports, image])
    return True
    
def stop_container(name):
    subprocess.run(["docker kill", name])
    return True

def hello():
    print('Hello from Doockmy you installed version is: ', version)




