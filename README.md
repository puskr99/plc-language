int x = 10;
float y = 10.0;
int z;
string ok;
bool hi = false;



print("Value of x is");
print(x);


int m = 5;

int func test(int x, const int y) {
    x = 10+y;
    return x;
}

int  a = test(m, 6);
print(a);
print(m);

if (test(m, 6) > 10){
   print("Greater than 10");
   print(test(m, 6));
}


while (x < 10){
   print("I am here");
   x = x+1;
}


if (x > 10) {
print("greater than 10");
}else {
print("less than 10");
}


if (true) {
print("Single if without else");
}