#ifndef NW_LIST
#define NW_LIST

//链表操作
#define list_init(head) 			\
	head = NULL						\

#define list_next(node)				\
	node = node == NULL ? NULL : node->next

#define list_tail(head, node) 		\
	node = head;					\
	while(node && node->next) node = node ->next 

#define list_insert(head, node) 	\
	node->next = (listnode*)head;	\
	head = (listhead)node

typedef struct _listnode
{
	void *ptr;
	struct _listnode *next;
}listnode;

typedef  listnode *listhead;

listnode *list_find(listhead head, void *ptr);

void list_remove(listhead *head, listnode *node);

void list_destroy(listhead *head);

void list_dump(listhead head);

#endif //end of NW_LIST