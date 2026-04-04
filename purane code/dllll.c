#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* prev;
    struct Node* next;
};

void display(struct Node* head) {
    struct Node* temp = head;
    printf("\nDoubly Linked List: ");
    while (temp != NULL) {
        printf("%d <-> ", temp->data);
        temp = temp->next;
    }
    printf("NULL\n");
}

struct Node* insertAtBeginning(struct Node* head, int data) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = data;
    newNode->prev = NULL;
    newNode->next = head;

    if (head != NULL)
        head->prev = newNode;

    head = newNode;
    printf("\nInserted %d at the beginning.\n", data);
    return head;
}

struct Node* deleteAtEnd(struct Node* head) {
    if (head == NULL) {
        printf("\nList is empty. Nothing to delete.\n");
        return head;
    }

    struct Node* temp = head;

    if (temp->next == NULL) {
        printf("\nDeleted %d from the end.\n", temp->data);
        free(temp);
        return NULL;
    }

    while (temp->next != NULL)
        temp = temp->next;

    printf("\nDeleted %d from the end.\n", temp->data);
    temp->prev->next = NULL;
    free(temp);

    return head;
}

int main() {
    struct Node* head = NULL;

    head = insertAtBeginning(head, 50);
    head = insertAtBeginning(head, 40);
    head = insertAtBeginning(head, 60);
    display(head);

    head = deleteAtEnd(head);
    display(head);

    head = deleteAtEnd(head);
    display(head);

    head = deleteAtEnd(head);
    display(head);

    head = deleteAtEnd(head);

    return 0;
}
