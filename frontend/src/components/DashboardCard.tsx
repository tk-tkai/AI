export default function DashboardCard({ title, children }: { title: string, children: React.ReactNode }) {
  return (
    <div className="p-6 bg-white border border-gray-200 rounded-lg shadow-sm">
      <h3 className="mb-2 text-lg font-semibold text-gray-700">{title}</h3>
      <div className="text-gray-900">
        {children}
      </div>
    </div>
  )
}