import React, { useState } from 'react';
import Home from './components/Home';
import Questionnaire from './components/Questionnaire';
import Results from './components/Results';

interface Response {
  question_id: number;
  response_value: number;
}

function App() {
  const [currentPage, setCurrentPage] = useState<'home' | 'questionnaire' | 'results'>('home');
  const [userResponses, setUserResponses] = useState<Response[]>([]);
  const [recommendationData, setRecommendationData] = useState<any>(null);

  const handleStartTest = () => {
    setCurrentPage('questionnaire');
  };

  const handleSubmitResponses = async (responses: Response[]) => {
    setUserResponses(responses);
    setCurrentPage('results');

    try {
      const sessionId = localStorage.getItem('sessionId') || `session-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
      localStorage.setItem('sessionId', sessionId);

      const response = await fetch('http://localhost:8000/recommend/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ session_id: sessionId, responses: responses }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setRecommendationData(data);
    } catch (error) {
      console.error("Error submitting responses or getting recommendations:", error);
      // Handle error state in UI
    }
  };

  const handleGoHome = () => {
    setCurrentPage('home');
    setRecommendationData(null); // Reset recommendation data when going home
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center">
      {currentPage === 'home' && <Home onStartTest={handleStartTest} />}
      {currentPage === 'questionnaire' && <Questionnaire onSubmit={handleSubmitResponses} />}
      {currentPage === 'results' && <Results recommendationData={recommendationData} onGoHome={handleGoHome} />}
    </div>
  );
}

export default App;
