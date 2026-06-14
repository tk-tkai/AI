const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/signals`);

export const getMarketStatus = async () => {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/signals`);
  if (!res.ok) throw new Error('Failed to fetch market data');
  return res.json();
};