import React from 'react';

interface HomeProps {
  onStartTest: () => void;
}

const Home: React.FC<HomeProps> = ({ onStartTest }) => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 text-white p-4">
      <h1 className="text-5xl md:text-7xl font-extrabold text-center mb-6 drop-shadow-lg">
        나만의 게임 추천 심리 테스트
      </h1>
      <p className="text-xl md:text-2xl text-center mb-10 leading-relaxed">
        당신의 성격과 워크 스타일을 분석하여, 당신에게 가장 잘 어울리는 게임을 추천해 드립니다.
        새로운 게임 경험을 발견하고 싶다면 지금 바로 시작하세요!
      </p>
      <button
        onClick={onStartTest}
        className="px-12 py-5 bg-white text-purple-700 font-bold text-xl rounded-full shadow-lg hover:bg-gray-100 hover:scale-105 transition-all duration-300 ease-in-out focus:outline-none focus:ring-4 focus:ring-white focus:ring-opacity-50"
      >
        테스트 시작하기
      </button>
    </div>
  );
};

export default Home;
