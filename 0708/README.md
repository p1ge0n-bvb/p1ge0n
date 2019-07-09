# 0708

由于虚拟机出现了一些问题，所以重新安装了一个ubuntu18.04版本的虚拟机，并对其进行了一些配置

## 安装pwntools

pip install pwntools --user

## 安装zsh和oh-my-zsh

### 安装zsh

sudo apt-get install zsh

chsh -s /bin/zsh（不要用sudo）

sudo vim /etc/passwd

将第一行/bin/bash改成/bin/zsh，最后一行/bin/bash改成/bin/zsh

### 安装oh-my-zsh

sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"

### 安装自动跳转插件autojump

sudo apt-get install autojump

配置：

vim .zshrc

在最后一行加入 . /usr/share/autojump/autojump.sh

source ~/.zshrc

### 安装zsh-syntax-highlighting语法高亮插件

git clone https://github.com/zsh-users/zsh-syntax-highlighting.git

echo "source \${(q-)PWD}/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> \${ZDOTDIR:-$HOME}/.zshrc

source ~/.zshrc

### 安装zsh-autosuggestions语法历史记录插件

git clone git://github.com/zsh-users/zsh-autosuggestions $ZSH_CUSTOM/plugins/zsh-autosuggestions

vim ~/.zshrc

在plugins处添加zsh-autosuggestions

在最后一行添加source $ZSH_CUSTOM/plygins/zsh-autosuggestions/zsh-autosuggestions.zsh

source ~/.zshrc