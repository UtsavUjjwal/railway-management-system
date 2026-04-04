#include<stdio.h>
#include<stdlib.h>

struct node {
    int data ;
    struct node * next;
};
void travesal (struct node*ptr){
    while (ptr != NULL){
    printf(" %d  element in list \n ", ptr-> data);
    ptr = ptr->next ;
    }
}

int main (){
    struct node * head ;
    struct node * second  ;
    struct node * third ;
    struct node * fourth ;
    head = (struct node *)malloc(sizeof(struct node)); 
    second = (struct node *)malloc(sizeof(struct node));
    third = (struct node *)malloc(sizeof(struct node));
    fourth = (struct node *)malloc(sizeof(struct node));



    head->data = 50;
    head->next = second;

    second->data = 40 ;
    second->next = third;

    third->data=30;
    third->next = fourth;
    
    fourth->data=3;
    fourth->next = NULL;
    
    travesal(head);
    



    



    return 0;
}