import React, { useState, useEffect } from 'react';

interface Question {
  id: number;
  text: string;
}

interface Response {
  question_id: number;
  response_value: number | null; // Allow null for no selection
}

interface QuestionnaireProps {
  onSubmit: (responses: Response[]) => void;
}

const responseLabels: { [key: number]: string } = {
  1: '전혀 그렇지 않다',
  2: '그렇지 않다',
  3: '보통이다',
  4: '그렇다',
  5: '매우 그렇다',
};

const Questionnaire: React.FC<QuestionnaireProps> = ({ onSubmit }) => {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [responses, setResponses] = useState<Response[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [isFading, setIsFading] = useState(false);

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const response = await fetch('http://localhost:8000/questions/');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data: Question[] = await response.json();
        setQuestions(data);
        // Initialize responses with null for no default selection
        setResponses(data.map(q => ({ question_id: q.id, response_value: null })));
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
  }, []);

  const handleResponseChange = (questionId: number, value: number) => {
    setResponses(prevResponses =>
      prevResponses.map(res =>
        res.question_id === questionId ? { ...res, response_value: value } : res
      )
    );
  };

  const handleNext = () => {
    // Check if the current question has been answered
    const currentResponse = responses.find(res => res.question_id === currentQuestion.id);
    if (currentResponse?.response_value === null) {
      // Optionally, show a warning to the user
      alert('질문에 응답해주세요!');
      return;
    }

    if (currentQuestionIndex < questions.length - 1) {
      setIsFading(true);
      setTimeout(() => {
        setCurrentQuestionIndex(prevIndex => prevIndex + 1);
        setIsFading(false);
      }, 300); // Match animation duration
    }
  };

  const handlePrev = () => {
    if (currentQuestionIndex > 0) {
      setIsFading(true);
      setTimeout(() => {
        setCurrentQuestionIndex(prevIndex => prevIndex - 1);
        setIsFading(false);
      }, 300); // Match animation duration
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Final check before submitting
    const allAnswered = responses.every(res => res.response_value !== null);
    if (!allAnswered) {
      alert('모든 질문에 응답해주세요!');
      return;
    }
    onSubmit(responses);
  };

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen text-xl text-gray-700">질문을 불러오는 중입니다...</div>;
  }

  if (error) {
    return <div className="flex items-center justify-center min-h-screen text-xl text-red-500">오류: {error}</div>;
  }

  const currentQuestion = questions[currentQuestionIndex];
  const currentResponseValue = responses.find(res => res.question_id === currentQuestion.id)?.response_value;
  const progressPercentage = ((currentQuestionIndex + 1) / questions.length) * 100;

  return (
    <div className="w-full max-w-3xl mx-auto p-8 bg-white shadow-2xl rounded-xl my-8">
      <h2 className="text-4xl font-extrabold text-center text-gray-800 mb-6">당신의 성향을 파악하는 질문</h2>
      
      {/* Progress Bar */}
      <div className="w-full bg-gray-200 rounded-full h-2.5 mb-8">
        <div className="bg-blue-600 h-2.5 rounded-full transition-all duration-500 ease-out" style={{ width: `${progressPercentage}%` }}></div>
      </div>

      <form onSubmit={handleSubmit}>
        <div 
          key={currentQuestion.id} 
          className={`transition-opacity duration-300 ${isFading ? 'opacity-0' : 'opacity-100'}`}
        >
          <div className="mb-8 p-6 border border-gray-200 rounded-lg bg-gray-50">
            <p className="text-2xl font-semibold text-gray-800 mb-6 text-center h-20 flex items-center justify-center">
              {currentQuestionIndex + 1}. {currentQuestion.text}
            </p>
            <div className="grid grid-cols-5 gap-2 mt-4"> {/* Use grid for better layout */}
              {[1, 2, 3, 4, 5].map(value => (
                <label 
                  key={value} 
                  className={`flex flex-col items-center justify-center p-2 rounded-lg cursor-pointer transition-all duration-200 text-center text-sm font-medium
                             ${currentResponseValue === value 
                                ? 'bg-blue-600 text-white shadow-lg scale-105' 
                                : 'bg-white text-gray-700 border-2 border-gray-300 hover:border-blue-500 hover:shadow-md'}`}
                >
                  <input
                    type="radio"
                    name={`question-${currentQuestion.id}`}
                    value={value}
                    checked={currentResponseValue === value}
                    onChange={() => handleResponseChange(currentQuestion.id, value)}
                    className="hidden" // Hide the native radio button
                  />
                  <span>{responseLabels[value]}</span>
                </label>
              ))}
            </div>
          </div>
        </div>

        <div className="flex justify-between items-center mt-10">
          <button
            type="button"
            onClick={handlePrev}
            disabled={currentQuestionIndex === 0}
            className="px-8 py-3 bg-gray-300 text-gray-800 font-bold rounded-full shadow-md hover:bg-gray-400 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            이전
          </button>

          {currentQuestionIndex === questions.length - 1 ? (
            <button
              type="submit"
              disabled={currentResponseValue === null} // Disable submit if not answered
              className="px-10 py-4 bg-gradient-to-r from-green-500 to-blue-600 text-white font-bold text-xl rounded-full shadow-lg hover:from-green-600 hover:to-blue-700 hover:scale-105 transition-all duration-300 ease-in-out disabled:opacity-50 disabled:cursor-not-allowed"
            >
              결과 보기
            </button>
          ) : (
            <button
              type="button"
              onClick={handleNext}
              disabled={currentResponseValue === null} // Disable next if not answered
              className="px-8 py-3 bg-blue-600 text-white font-bold rounded-full shadow-md hover:bg-blue-700 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              다음
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default Questionnaire;