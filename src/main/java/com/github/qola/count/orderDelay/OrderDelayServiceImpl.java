package com.github.qola.count.orderDelay;

import org.springframework.stereotype.Service;

import java.util.concurrent.ConcurrentHashMap;

/**
 * 동일한 주문이 한꺼번에 몰릴 경우 부하를 분산 하기 위한 용도로 사용.
 */
@Service
public class OrderDelayServiceImpl implements OrderDelayService {
    private long expireTime;
    private ConcurrentHashMap<Long, Integer> orderCountMap = new ConcurrentHashMap<Long, Integer>();

    @Override
    public int getOrderDelayTime(long coupangSrl){
        checkAndResetExpireTime();
        addOrderCount(coupangSrl);
        return getDelaySec(coupangSrl);
    }

    private int getDelaySec(long coupangSrl) {
        Integer currentCount = orderCountMap.get(coupangSrl);
        if(currentCount ==null || currentCount < OrderDelayConfig.DELAY_STATUS_THRESHOD){
            return 0;
        }
        return OrderDelayConfig.DELAY_SEC;
    }

    private void addOrderCount(long coupangSrl) {
        int cnt =1;
        Integer currentCount = orderCountMap.get(coupangSrl);
        if(currentCount !=null){
            cnt = currentCount +1;
        }
        orderCountMap.put(coupangSrl, cnt);
    }

    // Expire Time 초과시 map을 clear 하고 ExpireTime 재설정
    private void checkAndResetExpireTime() {
        if(expireTime < System.currentTimeMillis()){
            orderCountMap.clear();
            expireTime = System.currentTimeMillis() + OrderDelayConfig.EXPIRE_INTERVAL_SEC * 1000;
        }
    }
}
