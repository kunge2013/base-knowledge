#!/bin/bash

# Tmux 快速查询脚本 - 表格版

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# 表格参数
COL1_WIDTH=18
COL2_WIDTH=45
TABLE_WIDTH=$((COL1_WIDTH + COL2_WIDTH + 3))

# 打印表格分隔线
print_line() {
    printf "${CYAN}+"
    printf "%${COL1_WIDTH}s" | tr ' ' '-'
    printf "+"
    printf "%${COL2_WIDTH}s" | tr ' ' '-'
    printf "+${NC}\n"
}

# 打印表格标题行
print_table_header() {
    printf "${CYAN}|${NC}"
    printf "${BOLD}${GREEN}%-${COL1_WIDTH}s${NC}" "快捷键"
    printf "${CYAN}|${NC}"
    printf "${BOLD}${YELLOW}%-${COL2_WIDTH}s${NC}" "说明"
    printf "${CYAN}|${NC}\n"
}

# 打印表格内容行
print_table_row() {
    local key="$1"
    local desc="$2"
    printf "${CYAN}|${NC}"
    printf "${GREEN}%-${COL1_WIDTH}s${NC}" "$key"
    printf "${CYAN}|${NC}"
    printf "%-${COL2_WIDTH}s" "$desc"
    printf "${CYAN}|${NC}\n"
}

# 打印完整表格
print_table() {
    local title="$1"
    local rows=("${@:2}")

    echo ""
    echo -e "${BOLD}${BLUE}  $title${NC}"
    print_line
    print_table_header
    print_line

    for row in "${rows[@]}"; do
        local key="${row%%|*}"
        local desc="${row#*|}"
        print_table_row "$key" "$desc"
    done

    print_line
    echo ""
}

# 显示主菜单
show_menu() {
    clear
    echo -e "${RED}"
    cat << "EOF"
  ____  __  __          _____   _____ _    ___     __
 |  _ \|  \/  |   /\   |  __ \ / ____| |  | \ \   / /
 | |_) | \  / |  /  \  | |  | | |    | |__| |\ \_/ /
 |  _ <| |\/| | / /\ \ | |  | | |    |  __  | \   /
 | |_) | |  | |/ ____ \| |__| | |____| |  | |  | |
 |____/|_|  |_/_/    \_\_____/ \_____|_|  |_|  |_|
EOF
    echo -e "${NC}"

    echo -e "${GREEN}前缀键: ${YELLOW}Ctrl+a${NC} (默认为 Ctrl+b)"
    echo ""

    print_table "选择要查看的内容" \
        "1|会话管理" \
        "2|窗口管理" \
        "3|窗格管理" \
        "4|复制模式" \
        "5|命令行操作" \
        "6|实用技巧" \
        "7|显示全部" \
        "0|退出"

    echo -ne "${YELLOW}请输入选项 [0-7]: ${NC}"
}

# 会话管理
show_session_keys() {
    print_table "会话管理快捷键 (Ctrl+a + ...)" \
        "d|分离当前会话（后台运行）" \
        "s|列出所有会话" \
        "$|重命名会话" \
        "(|切换到上一个会话" \
        ")|切换到下一个会话" \
        "L|切换到上一个活跃会话"
}

# 窗口管理
show_window_keys() {
    print_table "窗口管理快捷键 (Ctrl+a + ...)" \
        "c|创建新窗口" \
        "n|切换到下一个窗口" \
        "p|切换到上一个窗口" \
        "0-9|切换到指定编号窗口" \
        ",|重命名当前窗口" \
        "&|关闭当前窗口" \
        "w|显示窗口列表" \
        "f|模糊搜索窗口"
}

# 窗格管理
show_pane_keys() {
    print_table "窗格管理快捷键 (Ctrl+a + ...)" \
        "||垂直分屏（左右）" \
        "-|水平分屏（上下）" \
        "方向键|在窗格间切换" \
        "o|切换到下一个窗格" \
        "x|关闭当前窗格" \
        "z|最大化/还原当前窗格" \
        "q|显示窗格编号（按数字快速跳转)" \
        "Space|切换窗格布局"

    print_table "调整窗格大小 (Ctrl+a + ...)" \
        "Shift+Left|向左扩大窗格" \
        "Shift+Right|向右扩大窗格" \
        "Shift+Up|向上扩大窗格" \
        "Shift+Down|向下扩大窗格"
}

# 复制模式
show_copy_keys() {
    print_table "复制模式操作" \
        "Ctrl+a [|进入复制模式" \
        "Ctrl+a ]|粘贴内容"

    print_table "复制模式内部命令 (Vi 风格)" \
        "v|开始选择文本" \
        "V|选择整行" \
        "Ctrl+v|矩形选择" \
        "y|复制选中内容到剪贴板" \
        "q|退出复制模式" \
        "/|向下搜索" \
        "?|向上搜索" \
        "n|下一个搜索结果" \
        "N|上一个搜索结果"
}

# 命令行操作
show_cli_commands() {
    print_table "会话管理命令" \
        "tmux new -s <名称>|创建新会话" \
        "tmux ls|列出所有会话" \
        "tmux attach -t <名称>|连接到会话 (可简写 tmux a)" \
        "tmux detach|分离会话" \
        "tmux kill-session -t <名称>|终止会话" \
        "tmux kill-server|终止所有会话"

    print_table "窗口和窗格命令" \
        "tmux split-window -h|垂直分屏" \
        "tmux split-window -v|水平分屏" \
        "tmux send-keys -t <会话> 'cmd' Enter|发送命令"
}

# 实用技巧
show_tips() {
    print_table "同步窗格输入" \
        ":setw synchronize-panes on|开启同步 (多窗格同时输入)" \
        ":setw synchronize-panes off|关闭同步"

    print_table "其他技巧" \
        "Ctrl+a r|重载 ~/.tmux.conf" \
        "Ctrl+a :|进入命令模式" \
        "bind c new-window -c '#{pane_current_path}'|新窗口保持当前目录"
}

# 显示全部
show_all() {
    show_session_keys
    read -p "按 Enter 继续..."
    show_window_keys
    read -p "按 Enter 继续..."
    show_pane_keys
    read -p "按 Enter 继续..."
    show_copy_keys
    read -p "按 Enter 继续..."
    show_cli_commands
    read -p "按 Enter 继续..."
    show_tips
}

# 搜索功能
search_keys() {
    local keyword="$1"
    local found=0

    echo ""
    echo -e "${BOLD}${BLUE}搜索结果: ${keyword}${NC}"
    echo ""

    # 定义所有快捷键数据
    local all_data=(
        "会话管理|d|分离当前会话"
        "会话管理|s|列出所有会话"
        "会话管理|$|重命名会话"
        "会话管理|(|切换到上一个会话"
        "会话管理|)|切换到下一个会话"
        "会话管理|L|切换到上一个活跃会话"
        "窗口管理|c|创建新窗口"
        "窗口管理|n|切换到下一个窗口"
        "窗口管理|p|切换到上一个窗口"
        "窗口管理|0-9|切换到指定编号窗口"
        "窗口管理|,|重命名当前窗口"
        "窗口管理|&|关闭当前窗口"
        "窗口管理|w|显示窗口列表"
        "窗口管理|f|模糊搜索窗口"
        "窗格管理|||垂直分屏"
        "窗格管理|-|水平分屏"
        "窗格管理|方向键|在窗格间切换"
        "窗格管理|o|切换到下一个窗格"
        "窗格管理|x|关闭当前窗格"
        "窗格管理|z|最大化/还原当前窗格"
        "窗格管理|q|显示窗格编号"
        "窗格管理|Space|切换窗格布局"
        "窗格大小|Shift+方向键|调整窗格大小"
        "复制模式|[|进入复制模式"
        "复制模式|]|粘贴内容"
        "复制模式|v|开始选择文本"
        "复制模式|V|选择整行"
        "复制模式|Ctrl+v|矩形选择"
        "复制模式|y|复制选中内容"
        "复制模式|q|退出复制模式"
        "复制模式|/|向下搜索"
        "复制模式|?|向上搜索"
        "复制模式|n|下一个搜索结果"
        "复制模式|N|上一个搜索结果"
        "CLI|tmux new -s|创建新会话"
        "CLI|tmux ls|列出所有会话"
        "CLI|tmux attach|连接到会话"
        "CLI|tmux detach|分离会话"
        "CLI|tmux kill-session|终止会话"
        "CLI|tmux split-window|分屏"
        "技巧|synchronize-panes|同步窗格输入"
        "技巧|r|重载配置文件"
    )

    printf "${CYAN}+------+------------------+----------------------+${NC}\n"
    printf "${CYAN}|${NC}${BOLD}${GREEN}%-6s${NC}${CYAN}|${NC}${BOLD}${GREEN}%-18s${NC}${CYAN}|${NC}${BOLD}${YELLOW}%-20s${NC}${CYAN}|${NC}\n" "分类" "快捷键" "说明"
    printf "${CYAN}+------+------------------+----------------------+${NC}\n"

    for item in "${all_data[@]}"; do
        local category="${item%%|*}"
        local rest="${item#*|}"
        local key="${rest%%|*}"
        local desc="${rest#*|}"

        if [[ "$category" =~ "$keyword" || "$key" =~ "$keyword" || "$desc" =~ "$keyword" ]]; then
            printf "${CYAN}|${NC}${RED}%-6s${NC}${CYAN}|${NC}${GREEN}%-18s${NC}${CYAN}|${NC}%-20s${CYAN}|${NC}\n" "$category" "$key" "$desc"
            found=$((found + 1))
        fi
    done

    printf "${CYAN}+------+------------------+----------------------+${NC}\n"
    echo ""
    echo -e "找到 ${GREEN}${found}${NC} 条匹配结果"
}

# 主函数
main() {
    local mode="${1:-menu}"
    local keyword="${2:-}"

    case "$mode" in
        session) show_session_keys ;;
        window)  show_window_keys ;;
        pane)    show_pane_keys ;;
        copy)    show_copy_keys ;;
        cli)     show_cli_commands ;;
        tips)    show_tips ;;
        all)     show_all ;;
        grep|search|find|s)
            if [ -z "$keyword" ]; then
                echo -e "${RED}用法: $0 grep <关键词>${NC}"
                echo -e "${YELLOW}示例: $0 grep 分屏${NC}"
                exit 1
            fi
            search_keys "$keyword"
            ;;
        *)
            while true; do
                show_menu
                read -r choice
                case "$choice" in
                    1) clear; show_session_keys; read -p "按 Enter 返回..." ;;
                    2) clear; show_window_keys; read -p "按 Enter 返回..." ;;
                    3) clear; show_pane_keys; read -p "按 Enter 返回..." ;;
                    4) clear; show_copy_keys; read -p "按 Enter 返回..." ;;
                    5) clear; show_cli_commands; read -p "按 Enter 返回..." ;;
                    6) clear; show_tips; read -p "按 Enter 返回..." ;;
                    7) clear; show_all; read -p "按 Enter 返回..." ;;
                    0|q|Q) echo -e "\n${GREEN}再见！${NC}"; exit 0 ;;
                    *) echo -e "\n${RED}无效选项${NC}"; sleep 1 ;;
                esac
            done ;;
    esac
}

# 执行入口
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
else
    tmux-help() { main "$@"; }
fi