#include <stdio.h>
#include <stdlib.h>

typedef struct Range {
	int64_t lo, hi;
	struct Range *next;
} Range;

int comp(const void *a, const void *b) {
	int64_t diff = ((Range*)a)->lo - ((Range*)b)->lo;
	if (diff < 0) return -1;
	if (diff > 0) return 1;
	return diff;
}

int main() {
	FILE *fp;
	if ((fp = fopen("input", "rt")) == NULL) {
		return 0;
	}

	char line[120];
	
	Range *head = NULL, *cur = NULL;
	int64_t lo, hi;
	while (fgets(line, sizeof(line), fp)) {
		if (sscanf(line, "%lld - %lld", &lo, &hi) != 2) {
			break;
		}
		if (head == NULL) {
			head = (Range*)malloc(sizeof(Range));
			cur = head;
			head->lo = lo;
			head->hi = hi;
			cur->next = NULL;
			continue;
		}
		cur->next = (Range*)malloc(sizeof(Range));
		cur->next->lo = lo;
		cur->next->hi = hi;
		cur->next->next = NULL;
		cur = cur->next;
	}

	/*
	
	For part 2 I'm just sort by creating a fixed size array

	*/

	Range intervals[500];
	int i = 0;
	for (cur = head; cur != NULL; cur = cur->next) {
		intervals[i].lo = cur->lo;
		intervals[i].hi = cur->hi;
		i++;
	}
	int n = i;

	qsort(intervals, n, sizeof(Range), comp);

	Range *un = NULL;
	for (i = 0; i < n; i++) {
		int64_t lo = intervals[i].lo;
		int64_t hi = intervals[i].hi;
		if (un == NULL) {
			un = (Range*)malloc(sizeof(Range));
			cur = un;
			un->lo = lo;
			un->hi = hi;
			cur->next = NULL;
			continue;
		}
		cur->next = (Range*)malloc(sizeof(Range));
		cur->next->lo = lo;
		cur->next->hi = hi;
		cur->next->next = NULL;
		cur = cur->next;
	}

	int merged = 0;
	do {
		merged = 0;
		for (cur = un; cur != NULL; cur = cur->next) {
			if (cur->next != NULL) {
				if (cur->next->lo <= cur->hi && cur->next->hi >= cur->hi) {
					cur->hi = cur->next->hi;
					cur->next = cur->next->next;
					merged++;
				} else if (cur->next->lo <= cur->hi && cur->next->hi <= cur->hi) {
					cur->next = cur->next->next;
					merged++;
				}
			}
		}
	} while (merged != 0);
	
	unsigned long long count = 0;
	for (cur = un; cur != NULL; cur = cur->next) {
		int64_t diff = cur->hi - cur->lo + 1;
		count += diff;
	}
	printf("count (part 2 answer): %lld\n", count);

	int64_t avail, avail_count = 0;
	cur = un;
	while (fgets(line, sizeof(line), fp)) {
		sscanf(line, "%lld", &avail);
		for (cur = un; cur != NULL; cur = cur->next) {
			if (avail >= cur->lo && avail <= cur->hi) {
				avail_count++;
				break;
			}
		}
		cur = un;
	}

	printf("part 1 answer: %lld\n", avail_count);

	fclose(fp);
	return 0;
}
