import os
import subprocess


def checkHasNodeEnv():
    status = os.system('node -v')
    return status == 0


def checkHasPrettier():
    status = os.system('prettier -v')
    return status == 0


def installPrettier():
    raise Exception('没得Prettier 你玩个毛')


def format(path):
    try:
        buffer = cmd("prettier " + path)
        return buffer

    except Exception as e:
        print('格式化出错：' + e)


def cmd(command):
    new_env = os.environ.copy()
    new_env['MEGAVARIABLE'] = 'MEGAVALUE'

    subp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            encoding="utf-8", env=new_env)
    subp.wait(5)
    out, err = subp.communicate()
    # for line in out.splitlines():
    #     print(line)
    # for line in err.splitlines():
    #     print(line)
    return out


if __name__ == '__main__':
    cmd('dir')
    cmd("java -version")
    cmd("node -v")
    cmd("prettier --help")
    cmd("yarn -v")
