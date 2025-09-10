#!/bin/bash

# 音乐工具 Docker 管理脚本

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 帮助信息
show_help() {
    echo -e "${BLUE}音乐工具 Docker 管理脚本${NC}"
    echo ""
    echo "用法:"
    echo "  ./docker-manage.sh [命令]"
    echo ""
    echo "命令:"
    echo -e "  ${GREEN}build${NC}     构建 Docker 镜像"
    echo -e "  ${GREEN}start${NC}     启动容器"
    echo -e "  ${GREEN}stop${NC}      停止容器"
    echo -e "  ${GREEN}restart${NC}   重启容器"
    echo -e "  ${GREEN}shell${NC}     进入容器 shell"
    echo -e "  ${GREEN}logs${NC}      查看容器日志"
    echo -e "  ${GREEN}status${NC}    查看工具状态"
    echo -e "  ${GREEN}clean${NC}     清理容器和镜像"
    echo -e "  ${GREEN}flac${NC}      运行 FLAC 分割工具"
    echo -e "  ${GREEN}m4s${NC}       运行 M4S 转换工具"
    echo ""
    echo "示例:"
    echo "  ./docker-manage.sh build"
    echo "  ./docker-manage.sh start"
    echo "  ./docker-manage.sh flac"
}

# 检查 Docker 是否安装
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}错误: 未找到 Docker，请先安装 Docker${NC}"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${YELLOW}警告: 未找到 docker-compose，将使用 docker 命令${NC}"
        return 1
    fi
    
    return 0
}

# 创建必要的目录
create_directories() {
    echo -e "${BLUE}创建必要的目录...${NC}"
    mkdir -p input output temp
    echo -e "${GREEN}目录创建完成${NC}"
}

# 构建镜像
build_image() {
    echo -e "${BLUE}构建 Docker 镜像...${NC}"
    
    if check_docker; then
        docker-compose build
    else
        docker build -t music-tool .
    fi
    
    echo -e "${GREEN}镜像构建完成${NC}"
}

# 启动容器
start_container() {
    create_directories
    
    echo -e "${BLUE}启动容器...${NC}"
    
    if check_docker; then
        docker-compose up -d
    else
        docker run -d \
            -v "$(pwd)/input:/app/input" \
            -v "$(pwd)/output:/app/output" \
            -v "$(pwd)/temp:/app/temp" \
            -v "$(pwd)/m4s:/app/m4s" \
            -v "$(pwd)/donglihuoche1:/app/donglihuoche1" \
            --name music-tool-container \
            music-tool
    fi
    
    echo -e "${GREEN}容器启动完成${NC}"
    echo -e "${YELLOW}使用 './docker-manage.sh shell' 进入容器${NC}"
}

# 停止容器
stop_container() {
    echo -e "${BLUE}停止容器...${NC}"
    
    if check_docker; then
        docker-compose down
    else
        docker stop music-tool-container 2>/dev/null || true
        docker rm music-tool-container 2>/dev/null || true
    fi
    
    echo -e "${GREEN}容器已停止${NC}"
}

# 重启容器
restart_container() {
    stop_container
    start_container
}

# 进入容器 shell
enter_shell() {
    echo -e "${BLUE}进入容器 shell...${NC}"
    
    if check_docker; then
        docker-compose exec music-tool bash
    else
        docker exec -it music-tool-container bash
    fi
}

# 查看日志
show_logs() {
    echo -e "${BLUE}查看容器日志...${NC}"
    
    if check_docker; then
        docker-compose logs -f music-tool
    else
        docker logs -f music-tool-container
    fi
}

# 查看状态
show_status() {
    echo -e "${BLUE}查看工具状态...${NC}"
    
    if check_docker; then
        docker-compose exec music-tool python music_tool_manager.py status
    else
        docker exec music-tool-container python music_tool_manager.py status
    fi
}

# 清理
clean_up() {
    echo -e "${BLUE}清理容器和镜像...${NC}"
    
    stop_container
    
    if check_docker; then
        docker-compose down --volumes --rmi all
    else
        docker rmi music-tool 2>/dev/null || true
    fi
    
    echo -e "${GREEN}清理完成${NC}"
}

# 运行 FLAC 工具
run_flac() {
    echo -e "${BLUE}运行 FLAC 分割工具...${NC}"
    
    if check_docker; then
        docker-compose exec music-tool python music_tool_manager.py flac
    else
        docker exec -it music-tool-container python music_tool_manager.py flac
    fi
}

# 运行 M4S 工具
run_m4s() {
    echo -e "${BLUE}运行 M4S 转换工具...${NC}"
    
    if check_docker; then
        docker-compose exec music-tool python music_tool_manager.py m4s
    else
        docker exec -it music-tool-container python music_tool_manager.py m4s
    fi
}

# 主逻辑
case "$1" in
    "build")
        build_image
        ;;
    "start")
        start_container
        ;;
    "stop")
        stop_container
        ;;
    "restart")
        restart_container
        ;;
    "shell")
        enter_shell
        ;;
    "logs")
        show_logs
        ;;
    "status")
        show_status
        ;;
    "clean")
        clean_up
        ;;
    "flac")
        run_flac
        ;;
    "m4s")
        run_m4s
        ;;
    *)
        show_help
        ;;
esac
