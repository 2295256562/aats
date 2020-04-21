#! /bin/sh
# $1 第一个参数
# $2 第二个参数
# "$*" 所有参数列表
# "$@" 所有参数列表

# ------------------上面是基本的语法-------------------------------

is_work=1
# $#:判断传递到脚本的参数个数： 项目绝对路径、启动端口
if [ $# != "2" ]
then
	# 如果不是2个参数，则输出一下信息，并且退出脚本
    echo "需要参数:  <project_dir> <runport>"
    is_work=0
fi

# 定义一个函数
run_temp_server(){
    project_dir=$1 # 传到函数的第一个参数：项目绝对路径
    runport=$2 # 第二个参数 端口

    # 检查绝对路径是否存在
    if [ ! -d $project_dir ]
    then
	# 项目不存在则输出以下信息
        echo "no such file or directory: $project_dir"

    else
		# 存在则执行下面命令
		echo "项目路径：$project_dir"
		echo "端口号：$runport"
		# 像在终端一样使用这些shell 命令
        cd $project_dir
  	    # 检查安装依赖包
#		pip3 install -r requirements.txt
		# 数据库迁移
#		python3 manage.py makemigrations
#    python3 manage.py migrate
		# 守护进程方式 启动celery
		# python3 manage.py celery multi start w1 -A QAPlatform  --loglevel=info
		python3 manage.py celery -B -A myCelery.main worker --loglevel=info
		# 启动项目 "&"表示后台运行
		python3 manage.py runserver 0.0.0.0:$runport &
		echo "启动成功"
    fi
}

if [ $is_work -eq "1" ]
then
    # 执行函数 并且传入参数
    run_temp_server  $1 $2
fi