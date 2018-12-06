/** Requirement:
 * 1. 将输入的数字当作字符串输入
 * 2. 将字符串存入数组中
 * 3. 利用函数，将数组中的信息输出
 *  读入一个浮点数值，将其转换为中文金额的大写方式，如123.45,转换为:壹佰贰拾叁元肆角伍分。要求：
 * （1）当金额为整数时，只表示整数部分，省略小数部分，并添加“整”字。例如，123表示为:壹佰贰拾叁元整；
 * （2）当金额中含有连续的0时，只需写一个“零”即可，例如， 10005表示为：壹万零伍元整；
 * （3）10的表示方式，例如，110元表示为：壹佰壹拾元整，而10则表示为：拾元整。
 * 提示：将字符串型转换为浮点型可以用Float.parseFloat(s)函数转换。
 * 三、实验要求
 * 1、能正确的进行数据转换；
 * 2、能在输入数据错误的情况下给出提示。
*/

/* #define TRANDITIONAL */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Constants definition */
/* U for units, T for tranditional name, D for digits. */
#ifndef TRANDITIONAL
    const char *U[] = {"大数", "无量大海", "不可思议", "那由他", "阿僧祗", "恒河沙",
                       "极", "载", "正", "涧", "沟", "穰", "秭", "垓", "京", "兆", "亿", "万"};
    const char *T[] = {"千", "百", "十", ""};
    const char *D[] = {"零", "一", "二", "三", "四", "五", "六", "七", "八", "九"};
    const char *X[] = {"角", "分"};
#else
    const char *U[] = {"大数", "无量大海", "不可思议", "那由他", "阿僧祗", "恒河沙",
                       "极", "载", "正", "涧", "沟", "穰", "秭", "垓", "京", "兆", "亿", "萬"};
    const char *T[] = {"仟", "佰", "拾", ""};
    const char *D[] = {"零", "壹", "贰", "叁", "肆", "伍", "陆", "柒", "捌", "镹"};
    const char *X[] = {"角", "分"};
#endif
#define NU 18           /* Number of Units */
#define NX 2            /* Number of decimal Units */
#define MAXNUMLEN 128   /* Max length of number string, store input */
#define MAXBUFLEN 1024  /* Max length of buffer size, store result. */

/* Operations */
char *_num2dec(char *dest, const char *n, int showCNY, int print_redundant_decimal) {
    const char *p = n;
    size_t raw_len = strlen(dest);
    while (*p) {
        int d = *p-'0';
        if (d || (!d && print_redundant_decimal)) {
            strcat(dest, D[*p-'0']);
            if (showCNY && p-n<NX) strcat(dest, X[p-n]);
        }
        p++;
    }
    if (print_redundant_decimal) {
        int i;
        for (i = 0; i < NX-(p-n); i++) {
            strcat(dest, D[0]);
            if (showCNY && p-n<NX) strcat(dest, X[p-n+i]);
        }
    }
    if (showCNY && strlen(dest) == raw_len) strcat(dest, "整");
    return dest;
}

/* Only process 4 digits of numbers */
char *_num2thou(char *dest, const char *n, int show_zero) {
    int len = strlen(n), i = 0, d, last_zero = 0;
    if (len > 4) return NULL;
    if (show_zero && len < 4) strcpy(dest, D[0]);
    while (i < len) {
        d = n[i]-'0';
        if (d) {
            if (last_zero) strcat(dest, D[last_zero=0]);
            strcat(dest, D[d]);
            strcat(dest, T[i + 4-len]);
        } else last_zero = 1;
        i++; // Foolish
    }
    return dest;
}

char *num2str_cny(char *dest, const char *n, int print_redundant_decimal) {
    int len = strlen(n), i;
    char *dp = strchr(n, '.');
    int ilen = dp ? dp-n : len;
    int fd = ilen % 4 ? ilen % 4 : 4, nblocks = (ilen-fd)/4; /* first digits */
    char _buf[5] = "";

    strncpy(_buf, n, fd);
    _num2thou(dest, _buf, 0);
    strcat(dest, U[NU-nblocks]);
    for (i = 0; i < nblocks; i++) {
        strncpy(_buf, n+fd+i*4, 4);
        _num2thou(dest, _buf, 1);
        if (i < nblocks-1) strcat(dest, U[NU-nblocks+i+1]);
    }
    strcat(dest, "元");
    if (dp) _num2dec(dest, n+ilen+1, 1, print_redundant_decimal);
    else strcat(dest, "整");
    return dest;
}


/* Error handler */
typedef enum {
    NO_ERR, FIRST_ZERO, FIRST_DOT, INVALID_CHAR,
    MULTIPLE_DOTS, TOO_MANY_DECIMALS, NEG_NOT_SUPPORT
} Err;
const char *ERR_INFO[] = {
    "",
    "Number should not start with char '0'.",
    "Number should not start with char '.'.",
    "Invalid char in your number.",
    "Multiple dots in your number.",
    "Too many decimals in your number.",
    "Negative number is not supported",
};

Err is_valid_num(const char *n) {
    int len = strlen(n), dot_pos = -1;
    if (len > 1 && n[0] == '0') return FIRST_ZERO;
    if (len > 1 && n[0] == '.') return FIRST_DOT;
    if (n[0] == '-') return NEG_NOT_SUPPORT;
    const char *p = n;
    while (*p) {
        if ((*p > '9' || *p < '0') && *p != '.')
            return INVALID_CHAR;
        if (*p == '.')
            if (dot_pos != -1) return MULTIPLE_DOTS;
            else dot_pos = p-n;
        else
            if (dot_pos != -1 && p-n-dot_pos > NX) return TOO_MANY_DECIMALS;
        p++;
    }
    return NO_ERR;
}

void err_handle(Err err_type) {
    if (err_type == NO_ERR) return ;
    fprintf(stderr, "%s\n", ERR_INFO[err_type]);
    exit(err_type);
}

char *get_input(char *buf) {
    char *p;
    fgets(buf, MAXNUMLEN, stdin);
    for (p = buf; *p; p++)
        ;
    p[-1] = 0;  // Eat the return key
    return buf;
}

char *remove_last_dot(char *num) {
    char *p = num+strlen(num)-1;
    if (*p == '.') *p = 0;
    return num;
}

int main(int argc, char *argv[]) {
    if (argc < 2) return 0;
    char buf[MAXBUFLEN] = "", num[MAXNUMLEN];
    strcpy(num, argv[1]);
    remove_last_dot(num);
    err_handle(is_valid_num(num));
    printf("%s\n", num2str_cny(buf, num, 0));

    return 0;
}
