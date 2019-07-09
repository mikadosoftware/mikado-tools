#! -*- coding:utf-8 -*-

"""
Using Xwindows, clean up a bit
"""
import subprocess

def touchpad():
    """FInd and disable touchpad on laptop

    Very specific to my laptop
    """
    nums = []
    out = subprocess.check_output(["xinput",])
    for line in out.split("\n"):
        if line.lower().find("touchpad") != -1:
            print(line, end=' ')
            for word in line.split():
                if word.find("id=") != -1:
                    num = word.replace("id=", "").strip()
                    print(num)
                    nums.append(num)
    nums.sort()
    touchpadid = nums[0]
    cmds = ["xinput", "--disable", touchpadid]
    print("running", cmds)
    out = subprocess.check_output(cmds)
    print(out)

if __name__ == '__main__':
    touchpad()
