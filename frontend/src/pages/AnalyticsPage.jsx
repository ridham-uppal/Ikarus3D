import React, { useState, useEffect } from 'react';
import Spinner from '../components/common/Spinner';
import ErrorDisplay from '../components/common/ErrorDisplay';
import StatCard from '../components/Analytics/StatCard';
import BarChartCard from '../components/Analytics/BarChartCard';
import PieChartCard from '../components/Analytics/PieChartCard';


const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

const AnalyticsPage = () => {
    const [analytics, setAnalytics] = useState(null);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchAnalytics = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/analytics`);
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                const data = await response.json();
                setAnalytics(data);
            } catch (e) {
                setError(e.message);
            } finally {
                setIsLoading(false);
            }
        };

        fetchAnalytics();
    }, []);

    if (isLoading) return <Spinner />;
    if (error) return <ErrorDisplay message={error} />;
    if (!analytics) return <p>No analytics data available.</p>;

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatCard title="Total Products" value={analytics.total_products} />
            <StatCard title="Average Price" value={`$${analytics.price_statistics.average}`} />
            <PieChartCard title="Top 5 Countries" data={analytics.top_countries} />
            <div className="col-span-1 md:col-span-2 lg:col-span-4">
                 <BarChartCard title="Top 10 Brands" data={analytics.top_brands} />
            </div>
            <div className="col-span-1 md:col-span-2 lg:col-span-4">
                 <BarChartCard title="Top 10 Materials" data={analytics.top_materials} />
            </div>
        </div>
    );
};

export default AnalyticsPage;
