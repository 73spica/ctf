import subprocess
import time
# http://maruton-memorandum.blogspot.jp/2013/05/windowscygwinrar.html

def do_unzip(target_file_path,source_path):
    cmd = "unzip %s -d %s"%(target_file_path,source_path)
    subprocess.call(cmd.split())

def do_unrar(target_file_path,source_path):
    cmd = "unrar e %s %s"%(target_file_path,source_path)
    subprocess.call(cmd.split())

def do_tar_xvzf(target_file_path,source_path):
    cmd = "tar xvzf %s -C %s"%(target_file_path,source_path)
    subprocess.call(cmd.split())

def check_file_type(target_file_path):
    cmd = "file %s"%target_file_path
    ret  =  subprocess.check_output( cmd.split(" ") )
    if "RAR" in ret:
        return "rar"
    elif "Zip" in ret:
        return "zip"
    elif "gzip" in ret:
        return "targz"

def do_ls(source_path):
    cmd = "ls %s"%source_path
    ret = subprocess.check_output(cmd.split())
    print ret
    return ret

def rename(target_file_path,file_type):
    if file_type=="targz":
        out_name = "%s.tar.gz"%target_file_path
        cmd = "mv %s %s"%(target_file_path,out_name)
        subprocess.call(cmd.split())
    else:
        out_name = target_file_path
    return out_name

def do_decompress():
    do_unzip("./100_00edb54bed7e46bd5cdb7c06059881c2.zip","./")
    source_path = "./work_folder/"
    for i in reversed(xrange(1,99+1)):
        target_file_path = source_path+str(i)
        file_type = check_file_type(target_file_path)
        if file_type == None:
            print "ERROR!!! Your program is missing."
            return
        print "[+] file type is %s"%file_type

        target_file_path = rename(target_file_path,file_type)
        print "[+] target:",target_file_path
        if file_type=="zip":
            do_unzip(target_file_path,source_path)
        elif file_type=="rar":
            do_unrar(target_file_path,source_path)
        elif file_type=="targz":
            do_tar_xvzf(target_file_path,source_path)

        if "work_folder" in do_ls(source_path):
            source_path += "work_folder/"
        # time.sleep(1)
        print "---------------------------------"


def main():
    do_decompress()


if __name__ == '__main__':
    main()