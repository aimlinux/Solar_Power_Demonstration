#include <stdio.h>

int main(void) {
    
    int a, b;
    int num;
    printf("1つ目の自然数を入力："); scanf("%d", &num);
    printf("2つ目の自然数を入力；"); scanf("%d", &b);
    a = num;

    int sum = 0;
    int mul = 1;

    if (a == b) {
        printf("同じ自然数が入力されました!");
    } else if (a <= 0 || b <= 0) {
        printf("自然数（0より大きな整数）以外が入力されました!");
    } else {

        for (int i = 0; i <= b - a + 1; i++) {
            sum = sum + a;
            mul = mul * a;
            a++;
        }
        printf("%dから%dまでの全整数の和は%d\n", num, b, sum);
        printf("%dから%dまでの全整数の積は%d\n", num, b, mul);
    }
    
    return 0;
}