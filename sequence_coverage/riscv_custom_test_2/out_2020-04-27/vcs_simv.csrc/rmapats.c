// file = 0; split type = patterns; threshold = 100000; total count = 0.
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include "rmapats.h"

void  hsG_0__0 (struct dummyq_struct * I1306, EBLK  * I1301, U  I691);
void  hsG_0__0 (struct dummyq_struct * I1306, EBLK  * I1301, U  I691)
{
    U  I1566;
    U  I1567;
    U  I1568;
    struct futq * I1569;
    struct dummyq_struct * pQ = I1306;
    I1566 = ((U )vcs_clocks) + I691;
    I1568 = I1566 & ((1 << fHashTableSize) - 1);
    I1301->I736 = (EBLK  *)(-1);
    I1301->I737 = I1566;
    if (0 && rmaProfEvtProp) {
        vcs_simpSetEBlkEvtID(I1301);
    }
    if (I1566 < (U )vcs_clocks) {
        I1567 = ((U  *)&vcs_clocks)[1];
        sched_millenium(pQ, I1301, I1567 + 1, I1566);
    }
    else if ((peblkFutQ1Head != ((void *)0)) && (I691 == 1)) {
        I1301->I739 = (struct eblk *)peblkFutQ1Tail;
        peblkFutQ1Tail->I736 = I1301;
        peblkFutQ1Tail = I1301;
    }
    else if ((I1569 = pQ->I1209[I1568].I751)) {
        I1301->I739 = (struct eblk *)I1569->I750;
        I1569->I750->I736 = (RP )I1301;
        I1569->I750 = (RmaEblk  *)I1301;
    }
    else {
        sched_hsopt(pQ, I1301, I1566);
    }
}
#ifdef __cplusplus
extern "C" {
#endif
void SinitHsimPats(void);
#ifdef __cplusplus
}
#endif
