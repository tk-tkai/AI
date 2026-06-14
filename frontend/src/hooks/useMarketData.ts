import { useQuery } from '@tanstack/react-query';
import { getMarketStatus } from '@/services/marketService';

export const useMarketData = () => {
  return useQuery({
    queryKey: ['marketData'],
    queryFn: getMarketStatus,
    refetchInterval: 5000, // อัปเดตข้อมูลทุก 5 วินาที
  });
};