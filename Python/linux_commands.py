"""
A python class file for the most usual linux commands.
"""
import subprocess
import os
import tempfile


class LinuxPython:

    def __init__(self,cmd,args):
        self.cmd = cmd
        self.args = args
        self.supress_print = False


    def exec_cmd(self):
        """
        Method that executes the linux command
            Returns:
                List containing the output of the specified command.
            Note: If the command doesn't have any form of output,
            this function will return None
        """
        match self.cmd:
            case "ls":
                return self.ls_command()
            case "touch":
                return self.touch_command()
            case "mv":
                return self.move_command()
            case "rm":
                return self.remove_command()
            case "ping":
                return self.ping_command()
            case "chmod":
                return self.chmod_command()
            case "cp":
                return self.cp_command()
            case "mkdir":
                return self.mkdir_command()
            case "ps":
                return self.ps_command()
            case "grep":
                return self.grep_command()
            case _:
                print("No match for " + self.cmd)
                return None


    def pipe_to(self, next_cmd):
        """
        Method to keep the | functionality from linux terminal
        """
        self.supress_print = True
        output = self.exec_cmd()

        if isinstance(output, list):
            output = '\n'.join(output)  # Join the lines into a single string

        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write(output)


        if not next_cmd.args:
            next_cmd.args = [None, None]
        elif len(next_cmd.args) < 2:
            next_cmd.args.append(None)

        next_cmd.args[1] = temp_file.name
        self.supress_print = False
        return next_cmd.exec_cmd()



    def ls_command(self):
        """
        A method to list the files in the current directory and
        parse the output.
        Equivalent command: ls [-args] [file_name]

        Returns:
            List containing the output of the ls command
        """
        try:
            cmd = 'ls'
            if len(self.args) == 1:
                args = self.args[0]
                temp = subprocess.Popen([cmd, args], stdout = subprocess.PIPE)
            else:
                args = self.args[0]
                filename = os.path.expandvars(self.args[1])
                temp = subprocess.Popen([cmd, args, filename], stdout=subprocess.PIPE)

            output = temp.communicate()[0].decode('utf-8')
            output_lines = output.split("\n")

            res=[]
            for line in output_lines:
                if not self.supress_print:
                    print(line)
                res.append(line)

            return res

        except:
            print("Encountered an error! PLease check again the arguments!")
            return None


    def remove_command(self):
        """
        Method for removing a file or directory.
        Equivalent command: rm file_or_directory

        Returns None
        """
        try:
            cmd = 'rm'
            args = self.args
            target = os.path.expandvars(args[0])
            subprocess.Popen([cmd, target], stdout=subprocess.PIPE)
            return None
        except:
            print("Encountered an error! Please check again the arguments!")
            return None


    def touch_command(self):
        """
        Method for creating an empty file or updating the access and modification times of a file.
        Equivalent command: touch file_name

        Returns None
        """
        try:
            cmd = 'touch'
            args = self.args
            filename = os.path.expandvars(args[0])
            subprocess.Popen([cmd, filename], stdout=subprocess.PIPE)
            return None
        except:
            print("Encountered an error! Please check again the arguments!")
            return None


    def move_command(self):
        """
        Method for moving or renaming files or directories.
        Equivalent command: mv source destination

        Returns None
        """
        try:
            cmd = 'mv'
            args = self.args
            source = os.path.expandvars(args[0])
            destination = os.path.expandvars(args[1])
            subprocess.Popen([cmd, source, destination], stdout=subprocess.PIPE)
            return None
        except:
            print("Encountered an error! Please check again the arguments!")
            return None


    def ping_command(self):
        """
        Method for pinging a specified host.
        Equivalent command: ping [-args] host
        Returns:
            List containing the output of the ping command
        """
        try:
            cmd = 'ping'
            args = self.args
            temp = subprocess.Popen([cmd, args[0], args[1]], stdout=subprocess.PIPE)
            output = str(temp.communicate())
            output = output.split("\n")
            output = output[0].split('\\')

            res = []
            for line in output:
                res.append(line)
                if not self.supress_print:
                    print(line)


            return res
        except:
            print("Encountered an error! PLease check again the arguments!")
            return None




    def chmod_command(self):
        """
        Method for changing the permissions of a specified file!
        It will also print the permissions before the change and after!
        Equivalent command: chmod

        Returns None
        """
        cmd = 'chmod'
        args = self.args[0]
        filename = os.path.expandvars(self.args[1])


        # print('File permissions before chmod % s: ' % (args))
        # ls_cmd = LinuxPython('ls', ['-l', filename])
        # ls_cmd.exec_cmd()


        subprocess.Popen([cmd, args, filename], stdout=subprocess.PIPE)
        # ls_cmd.exec_cmd()

        return None


    def cp_command(self):
        """
            Method for copying files or directories.
            Equivalent command: cp source destination

            Returns None
        """
        try:
            cmd = 'cp'
            args = self.args
            source = os.path.expandvars(args[0])
            destination = os.path.expandvars(args[1])
            subprocess.Popen([cmd, source, destination], stdout=subprocess.PIPE)
            return None

        except:
            print("Encountered an error! Please check again the arguments!")
            return None


    def mkdir_command(self):
        """
            Method for creating a new directory.
            Equivalent command: mkdir directory_name

            Returns None
        """
        try:
            cmd = 'mkdir'
            args = self.args
            directory_name = os.path.expandvars(args[0])
            subprocess.Popen([cmd, directory_name], stdout=subprocess.PIPE)
            return None
        except:
            print("Encountered an error! Please check again the arguments!")
            return None



    def ps_command(self):
        """
            Method for displaying information about active processes.
            Equivalent command: ps [-args]

            Returns:
                List containing the output of the ps command
        """
        try:
            cmd = 'ps'
            args = self.args
            temp = subprocess.Popen([cmd, *args], stdout=subprocess.PIPE)
            output = temp.communicate()[0].decode('utf-8')

            lines = output.split('\n')
            res = [' '.join(lines[0].split())]
            if not self.supress_print:
                print(res[0])

            i=1
            for line in lines[1:]:
                if line:
                    res.append(' '.join(line.split()))
                    if not self.supress_print:
                        print(res[i])
                    i+=1

            return res
        except:
            print("Encountered an error! Please check again the arguments!")
            return None




    def grep_command(self):
        """
            Method for searching a file or input for a pattern.
            Equivalent command: grep pattern [file]

            Returns:
                List containing the output of the grep command
        """
        try:
            cmd = 'grep'
            args = self.args
            pattern = args[0]

            if len(args) > 1:
                filename = os.path.expandvars(args[1])
                temp = subprocess.Popen([cmd, pattern, filename], stdout=subprocess.PIPE)
            else:
                temp = subprocess.Popen([cmd, pattern], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

            output = temp.communicate()[0].decode('utf-8')
            if not self.supress_print:
                print(output)
            return output

        except Exception as e:
            print("Encountered an error! Please check again the arguments!")
            return None



# Examples

#cmd1=LinuxPython("ls", ["-al", "$HOME/Desktop/output.txt"])
#equivalent linux terminal command: ls -al ~/Desktop/output.txt
#cmd1.exec_cmd()
#cmd1=LinuxPython("ls", ["-al"])
#cmd1.exec_cmd()
# cmd2=LinuxPython("chmod",["755","$HOME/Desktop/output.txt"])
#equivalent  linux terminal command: chmod 755 ~/Desktop/output.txt
# cmd2.exec_cmd()
# cmd3=LinuxPython("ps",[])
# cmd3.exec_cmd()
# cmd4=LinuxPython("mkdir",["$HOME/Desktop/sth2"])
# cmd4.exec_cmd()
# cmd5=LinuxPython("cp",["$HOME/Desktop/output2.txt", "$HOME/Desktop/ceva"])
# cmd5.exec_cmd()
# cmd_grep = LinuxPython("grep", ["Hello", "$HOME/Desktop/output2.txt"])
# cmd_grep.exec_cmd()
# cmd_remove = LinuxPython("rm", ["$HOME/Desktop/output.txt"])
# cmd_remove.exec_cmd()

# cmd_touch = LinuxPython("touch", ["$HOME/Desktop/new_file.txt"])
# cmd_touch.exec_cmd()

# cmd_move = LinuxPython("mv", ["$HOME/Desktop/new_file.txt", "$HOME/Desktop/ceva/"])
# cmd_move.exec_cmd()



# Example usage with piping
# ls_cmd = LinuxPython("ls", ["-al", "/"])
# ls_cmd.exec_cmd()
# grep_cmd = LinuxPython("grep", ["bin"])
## ps_cmd = LinuxPython("ps", ["aux"])
#
#
# ls_cmd.pipe_to(grep_cmd)
## ps_cmd.pipe_to(grep_cmd)




