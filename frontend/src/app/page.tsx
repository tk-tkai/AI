'use client'
import DashboardCard from '@/components/DashboardCard';
import { useMarketData } from '@/hooks/useMarketData';

export default function Dashboard() {
  const { data, isLoading, error } = useMarketData();

  if (isLoading) return <div>กำลังโหลดข้อมูลตลาด...</div>;
  if (error) return <div>เกิดข้อผิดพลาดในการเชื่อมต่อ</div>;

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold">Trading Dashboard</h1>
      <div className="mt-4 p-4 border rounded">
        <pre>{JSON.stringify(data, null, 2)}</pre>
      </div>
      <DashboardCard title="สถานะตลาดปัจจุบัน">
        {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : <p>กำลังโหลด...</p>}
      </DashboardCard>
    </main>
  );
}