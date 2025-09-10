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
    echo -e "  ${GREEN}start${NC}     启动 Web 界面容器"
    echo -e "  ${GREEN}stop${NC}      停止容器"
    echo -e "  ${GREEN}restart${NC}   重启容器"
    echo -e "  ${GREEN}shell${NC}     进入容器 shell (命令行模式)"
    echo -e "  ${GREEN}logs${NC}      查看容器日志"
    echo -e "  ${GREEN}status${NC}    查看工具状态"
    echo -e "  ${GREEN}clean${NC}     清理容器和镜像"
    echo -e "  ${GREEN}web${NC}       打开 Web 界面"
    echo -e "  ${GREEN}cli${NC}       启动命令行模式容器"
    echo ""
    echo "Web 界面:"
    echo -e "  ${YELLOW}启动后访问: http://localhost:5001${NC}"
    echo ""
    echo "示例:"
    echo "  ./docker-manage.sh build   # 构建镜像"
    echo "  ./docker-manage.sh start   # 启动 Web 界面"
    echo "  ./docker-manage.sh web     # 打开浏览器访问 Web 界面"
}

# 检查 Docker Compose 是否可用
check_docker_compose() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}错误: 未找到 Docker，请先安装 Docker${NC}"
        exit 1
    fi
    
    # 检查 docker compose (V2) 或 docker-compose (V1)
    if command -v docker-compose &> /dev/null; then
        COMPOSE_CMD="docker-compose"
    elif docker compose version &> /dev/null; then
        COMPOSE_CMD="docker compose"
    else
        echo -e "${YELLOW}警告: 未找到 docker-compose 或 docker compose，将使用 docker 命令${NC}"
        return 1
    fi
    
    echo -e "${GREEN}使用 Docker Compose: $COMPOSE_CMD${NC}"
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
    
    if check_docker_compose; then
        $COMPOSE_CMD build
    else
        docker build -t music-tool .
    fi
    
    echo -e "${GREEN}镜像构建完成${NC}"
}

# 启动容器
start_container() {
    create_directories
    
    echo -e "${BLUE}启动 Web 界面容器...${NC}"
    
    if check_docker_compose; then
        $COMPOSE_CMD up -d
    else
        docker run -d \
            -p 5000:5000 \
            -v "$(pwd)/input:/app/input" \
            -v "$(pwd)/output:/app/output" \
            -v "$(pwd)/temp:/app/temp" \
            -v "$(pwd)/uploads:/app/uploads" \
            -v "$(pwd)/m4s:/app/m4s" \
            -v "$(pwd)/donglihuoche1:/app/donglihuoche1" \
            --name music-tool-web \
            music-tool
    fi
    
    echo -e "${GREEN}容器启动完成${NC}"
    echo -e "${YELLOW}Web 界面地址: http://localhost:5001${NC}"
    echo -e "${YELLOW}使用 './docker-manage.sh web' 打开浏览器${NC}"
}

# 停止容器
stop_container() {
    echo -e "${BLUE}停止容器...${NC}"
    
    if check_docker_compose; then
        $COMPOSE_CMD down
    else
        docker stop music-tool-web 2>/dev/null || true
        docker rm music-tool-web 2>/dev/null || true
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
    
    if check_docker_compose; then
        $COMPOSE_CMD exec music-tool bash
    else
        docker exec -it music-tool-web bash
    fi
}

# 查看日志
show_logs() {
    echo -e "${BLUE}查看容器日志...${NC}"
    
    if check_docker_compose; then
        $COMPOSE_CMD logs -f music-tool
    else
        docker logs -f music-tool-web
    fi
}

# 查看状态
show_status() {
    echo -e "${BLUE}查看工具状态...${NC}"
    
    if check_docker_compose; then
        $COMPOSE_CMD exec music-tool python music_tool_manager.py status
    else
        docker exec music-tool-web python music_tool_manager.py status
    fi
}

# 打开 Web 界面
open_web() {
    echo -e "${BLUE}打开 Web 界面...${NC}"
    
    # 检查容器是否运行
    if check_docker_compose; then
        if ! $COMPOSE_CMD ps | grep -q "Up"; then
            echo -e "${YELLOW}容器未运行，正在启动...${NC}"
            start_container
            sleep 3
        fi
    else
        if ! docker ps | grep -q "music-tool-web"; then
            echo -e "${YELLOW}容器未运行，正在启动...${NC}"
            start_container
            sleep 3
        fi
    fi
    
    # 尝试打开浏览器
    if command -v open &> /dev/null; then
        # macOS
        open http://localhost:5001
    elif command -v xdg-open &> /dev/null; then
        # Linux
        xdg-open http://localhost:5001
    elif command -v start &> /dev/null; then
        # Windows
        start http://localhost:5001
    else
        echo -e "${GREEN}请在浏览器中访问: http://localhost:5001${NC}"
    fi
}

# 启动命令行模式
start_cli_mode() {
    create_directories
    
    echo -e "${BLUE}启动命令行模式容器...${NC}"
    
    if check_docker_compose; then
        # 临时覆盖 docker-compose 配置
        docker run -it --rm \
            -v "$(pwd)/input:/app/input" \
            -v "$(pwd)/output:/app/output" \
            -v "$(pwd)/temp:/app/temp" \
            -v "$(pwd)/uploads:/app/uploads" \
            -v "$(pwd)/m4s:/app/m4s" \
            -v "$(pwd)/donglihuoche1:/app/donglihuoche1" \
            --entrypoint bash \
            music-tool
    else
        docker run -it --rm \
            -v "$(pwd)/input:/app/input" \
            -v "$(pwd)/output:/app/output" \
            -v "$(pwd)/temp:/app/temp" \
            -v "$(pwd)/uploads:/app/uploads" \
            -v "$(pwd)/m4s:/app/m4s" \
            -v "$(pwd)/donglihuoche1:/app/donglihuoche1" \
            --entrypoint bash \
            --name music-tool-cli \
            music-tool
    fi
}

# 清理
clean_up() {
    echo -e "${BLUE}清理容器和镜像...${NC}"
    
    stop_container
    
    if check_docker_compose; then
        $COMPOSE_CMD down --volumes --rmi all
    else
        docker rmi music-tool 2>/dev/null || true
    fi
    
    echo -e "${GREEN}清理完成${NC}"
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
    "web")
        open_web
        ;;
    "cli")
        start_cli_mode
        ;;
    *)
        show_help
        ;;
esac
