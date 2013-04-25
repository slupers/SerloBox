/*		C No Evil Homework
Each question carries equal weight.

The assignment must be turned in and committed to your SVN by August 31, 2011
at 11:00am. No late submissions will be allowed.

Instructions on how to use SVN and other information relating to
online submission can be found on the course website.

http://www.cs.illinois.edu/class/cs241/handin.html
*/

/*
Part I
Each of these examples can appear inside C programs.

The ... means additional (irrelevant) instructions.

For each example, answer the following questions:
(a) What does the code attempt to do?

(b) Correct the code listed
 */


/*Goal: Attempts to create a pointer p that will point to x
 
*/
void Problem1(){
	int x;
	int *p = &x;
}


/*Goal: Have the memory address that p is pointing to contain the value 12.5

*/
void Problem2(){
	float *p = malloc(sizeof(float));
	*p = 12.5;
}


/*Goal: Check if a is between 0 and 1 (not including 0 and 1)

*/
void Problem3(){
	float a;
	...
	if(0 < a && a < 1)
		printf("a is a value between 0 and 1.\n");
}

/*Goal: Tries to check if x is equal to y

*/
void Problem4(){
	int x=5;
	int y;
	...
	if(x==y)	//corrected here
		printf("x and y are equal.\n");
	else
		printf("x and y are different.\n");
	
}

/*Goal: Trying to store int value at x into float variable y and have all the pointers point to the address where value of x is stored

*/
void Problem5(){
	int x, *ip;
	float y, *fp;
	...
	ip = &x;
	fp = &y;
	y = (float)x;
	//fp = (float*)ip;
	//y=*fp;
	
}

/*Goal: Condition supposed to be set so that loop is continued until a is equal to b

*/
void Problem6(){
	int a=0, b=10;
	while (a != b){	//corrected here
		...
		a++;
	}
	
}

/*Goal: Attemps to scan into array of chars of 30

*/
void Problem7(){
	char s[30];
	scanf("%29s",s);
	s[30] = '\0';
}


/*Goal: reset is attempting to reset the value of x to 0

*/
//Problem 8
void reset(int *x){
	*x=0;	//correction on this line
}

int main(){
	...
	int x=1;
	reset(&x);
	printf("x is now 0.\n");
	return 0;
}


/*Goal: Make a string of 50 chars

*/
void Problem9(){
	char *s = (char *) malloc (50);
	...
	strcpy(s,"this is a string";)
	free(s);
}

/*Goal: Store values into float array

*/
void Problem10(){
	float *values = malloc(10*sizeof(int));
	int i,n = 10;
	for(i=0;i<n;i++)
		values[i] = (float)i/n;
}

/*Goal: Fill array with values

*/
void Problem11(){
	int **array;
	int i,j;
	array = malloc(10*sizeof(int *));
	for(i=0;i<10;i++)
		for(j=0;j<10;j++)
			array[i] = malloc(10*sizeof(int));
			array[i][j] = i*j;
}

/*Goal: Set x to a value depending on what is entered into str string

*/
void Problem12(){
	char *str = (char *)malloc(10);
	int x;
	scanf("%9s",str);
	...
	switch(str) {
		case "blue":
			x=1; break;
		case "red":
			x=2; break;
		default: x=0;break;
	}
	free(str);
}

/*Goal: Depending on i, perform the necessary task

*/
void Problem13(){
	int i;
	...
	scanf("%d",&i);
	switch(i) {
		case 1: function1();break;
		case 2: function2();break;
		default: printf("Unknown command.\n");break;
	}
}


/*Goal: Apply the macros to calculate product and sum 

*/
void Problem14(){
	#define multiply(x,y)	((x)*(y))
	#define sum(x,y)	((x)+(y))
	int x = 3, y = 5;
	int z = 100 / multiply(x+1, y);
	z = 100 / sum(x*y, y);
	
}

/*Goal: Exit when an invalid value is given for x

*/
void Problem15(){
	int x;
	...
	if(x < 0){
		printf("invalid value.\n");
		exit(EXIT_FAILURE);
	}
}

/*Goal: make a string "abcd"

*/
void Problem16(){
	char str[5];
	strcat(str, "abcd");
}



/* Part II
Provide the code for the following functions.
You may use only the allowed operators specified in each problem.
You may not use any other operators, control constructs (if, do, while, ...),
or function calls.

You can only use constant values from 0L to 255L (0x0L to 0xFFL).

You may assume that your machine:
· Uses 2’s complement representation of integers
· Performs right shift arithmetically
· Uses either a 32- or a 64-bit representation of long integers
· Has unpredictable behavior when shifting a long integer by more
	than the word size

*/

long int clearBit(long int value, long int flag){
	/* returns value with all set bit positions from flag cleared
		using only the operators & ~ ^ | >> << ! + =
		
		For Example:  value=0xFF flag=0x55 -> retval=0xAA */

	// return (value) AND (COMPLEMENT flag)
	return (value)&(~flag);

}


long int isEqual(long int x, long int y){
	/* returns 1L if x==y, 0L otherwise
		using only the operators & ~ ^ | >> << ! + = */

	return !(x^y);

}
