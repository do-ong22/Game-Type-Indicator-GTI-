import React, { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';

interface Game {
  id: number;
  title: string;
  thumbnail: string;
  short_description: string;
  genre: string;
  platform: string;
  game_url: string;
}

interface RecommendationData {
  profile: {
    id: number;
    name: string;
    description: string;
    centroid_values: string;
  };
  recommended_games: Game[];
  recommendation_reason: string;
}

interface ResultsProps {
  recommendationData: RecommendationData | null;
  onGoHome: () => void;
}

const Results: React.FC<ResultsProps> = ({ recommendationData, onGoHome }) => {
  const chartRef = useRef<HTMLCanvasElement>(null);
  const chartInstance = useRef<Chart | null>(null);
  const [copySuccess, setCopySuccess] = useState<string>('');

  useEffect(() => {
    if (recommendationData && chartRef.current) {
      const ctx = chartRef.current.getContext('2d');
      if (!ctx) return;

      if (chartInstance.current) {
        chartInstance.current.destroy();
      }

      const profileCentroidValues = recommendationData.profile.centroid_values ? JSON.parse(recommendationData.profile.centroid_values) : [];
      
      const getDimensionAverages = (values: number[]) => {
        const averages = [];
        for (let i = 0; i < 5; i++) {
          const start = i * 3;
          const end = start + 3;
          const dimensionValues = values.slice(start, end);
          averages.push(dimensionValues.reduce((sum, val) => sum + val, 0) / dimensionValues.length);
        }
        return averages;
      };

      const profileDimensionAverages = getDimensionAverages(profileCentroidValues);

      const labels = [
        "의사결정 및 문제 해결",
        "대인 관계 및 협업",
        "도전 및 위험 감수",
        "정보 처리 및 집중",
        "학습 및 탐구"
      ];

      chartInstance.current = new Chart(ctx, {
        type: 'radar',
        data: {
          labels: labels,
          datasets: [
            {
              label: '당신의 프로필',
              data: profileDimensionAverages,
              backgroundColor: 'rgba(79, 70, 229, 0.4)',
              borderColor: 'rgba(79, 70, 229, 1)',
              borderWidth: 2,
              pointBackgroundColor: 'rgba(79, 70, 229, 1)',
              pointBorderColor: '#fff',
              pointHoverBackgroundColor: '#fff',
              pointHoverBorderColor: 'rgba(79, 70, 229, 1)'
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            r: {
              angleLines: { display: true, color: 'rgba(200, 200, 200, 0.2)' },
              grid: { color: 'rgba(200, 200, 200, 0.2)' },
              suggestedMin: 1,
              suggestedMax: 5,
              pointLabels: { font: { size: 14, weight: 'bold' }, color: '#333' },
              ticks: { stepSize: 1, display: false }
            }
          },
          plugins: {
            legend: { position: 'top', labels: { font: { size: 14 } } },
            title: { display: true, text: '당신의 워크 스타일 프로필', font: { size: 20, weight: 'bold' }, color: '#333' }
          }
        },
      });
    }
  }, [recommendationData]);

  const handleShare = async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      setCopySuccess('복사 완료!');
      setTimeout(() => setCopySuccess(''), 2000);
    } catch (err) {
      setCopySuccess('복사 실패!');
      console.error('Failed to copy: ', err);
    }
  };

  if (!recommendationData) {
    return <div className="flex items-center justify-center min-h-screen text-xl text-gray-700">분석 결과를 불러오는 중입니다...</div>;
  }

  const { profile, recommended_games, recommendation_reason } = recommendationData;

  return (
    <div className="mx-auto p-8 bg-white shadow-2xl rounded-xl my-8">
      <h2 className="text-4xl font-extrabold text-center text-gray-800 mb-6">당신의 워크 스타일 프로필</h2>
      <div className="text-center mb-10 p-6 bg-blue-50 rounded-lg border border-blue-200">
        <p className="text-3xl font-bold text-blue-700 mb-3">{profile.name}</p>
        <p className="text-gray-700 text-lg leading-relaxed">{profile.description}</p>
      </div>

      <div className="mb-10">
        <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center">당신의 프로필 분석</h3>
        <div className="relative h-96 w-full bg-gray-50 p-4 rounded-lg shadow-inner">
          <canvas ref={chartRef}></canvas>
        </div>
      </div>

      <div>
        <h3 className="text-2xl font-bold text-gray-800 mb-4 text-center">당신에게 추천하는 게임 장르</h3>
        <div className="text-center mb-8 p-4 bg-green-50 rounded-lg border border-green-200">
          <p className="text-gray-700 text-lg leading-relaxed">{recommendation_reason}</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {recommended_games.map((game) => (
            <div key={game.id} className="border border-gray-200 rounded-xl p-6 flex flex-col items-center text-center bg-white shadow-lg hover:shadow-xl transition-shadow duration-300">
              <img src={game.thumbnail} alt={game.title} className="w-40 h-40 object-cover rounded-lg mb-4 border border-gray-100" />
              <p className="text-2xl font-semibold text-gray-800 mb-2">{game.title}</p>
              <p className="text-gray-600 text-base mb-3">{game.genre} | {game.platform}</p>
              <p className="text-gray-700 text-sm leading-relaxed mb-4 flex-grow">{game.short_description}</p>
              <a 
                href={game.game_url} 
                target="_blank" 
                rel="noopener noreferrer" 
                className="mt-auto px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-700 text-white font-bold rounded-full shadow-md hover:from-purple-700 hover:to-indigo-800 hover:scale-105 transition-all duration-300 ease-in-out"
              >
                게임 보러가기
              </a>
            </div>
          ))}
        </div>
      </div>

      <div className="flex justify-center gap-4 mt-12">
        <button
          onClick={onGoHome}
          className="px-8 py-4 bg-gray-200 text-gray-800 font-bold rounded-full shadow-md hover:bg-gray-300 hover:scale-105 transition-all duration-300 ease-in-out"
        >
          홈으로 돌아가기
        </button>
        <button
          onClick={handleShare}
          className="px-8 py-4 bg-blue-500 text-white font-bold rounded-full shadow-md hover:bg-blue-600 hover:scale-105 transition-all duration-300 ease-in-out relative"
        >
          결과 공유하기
          {copySuccess && (
            <span className="absolute -top-8 left-1/2 -translate-x-1/2 bg-green-500 text-white text-xs px-2 py-1 rounded-md animate-fade-in-out">
              {copySuccess}
            </span>
          )}
        </button>
      </div>
    </div>
  );
};

export default Results;