#include "nw_list.h"

#include <stdlib.h>
#include <stdio.h>

listnode *
list_find(listhead head, void *ptr) 
{
	if (head == NULL || ptr == NULL) return NULL;

	listhead tmp = head;
	while(tmp) {
		if (tmp->ptr == ptr) {
			break;
		}
	}

	return tmp;
}

void 
list_remove(listhead *head, listnode *node) 
{
	if (*head == NULL || node == NULL) return ;

	if (node == *head) {
		*head = NULL;
		return ;
	}

	listnode *tmp = *head;

	while(tmp && tmp->next != node) list_next(node);

	if (tmp != NULL) tmp->next = node->next;
}

void 
list_destroy(listhead *head) 
{
	listhead tmphead = *head;
	while(tmphead) {
		listnode  *tmpnode = tmphead;
		tmphead = tmphead->next;
		free(tmpnode);
	}	
	
	head = NULL;
}

void 
list_dump(listhead head) 
{
	listhead tmp = head;

	while (tmp) {
		printf("cur:[%p], next:[%p]\n", tmp, tmp->next);
		list_next(tmp);
	}
}