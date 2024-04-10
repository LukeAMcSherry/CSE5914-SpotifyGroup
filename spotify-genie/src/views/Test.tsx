import React, { useEffect, useState } from 'react';
import '../styles/Home.css';
import '../styles/Features.css';

interface Recommendation {
  track_name: string;
  artist_name: string;
  image: string;
  track_link: string;
  
}

const Home = () => {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const res = await fetch('/display_reccommendations', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        if (!res.ok) {
          throw new Error(`Error: ${res.status}`);
        }
        const data = await res.json();
        setRecommendations(data);
      } catch (error) {
        console.error(error);
      }
    }
    fetchRecommendations();
  }, []);

  return (
    <div style={{ backgroundColor: '#EEFFEF', color: 'white', display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
      <div>
        <h2>Recommendations Table:</h2>
        <table style={{ border: '1px solid black', borderCollapse: 'collapse', backgroundColor: '#CBC3E3' }}>
          <thead>
            <tr>
              <th style={{ border: '1px solid black' }}>Image</th>
              <th style={{ border: '1px solid black' }}>Track</th>
            </tr>
          </thead>
          <tbody>
            {recommendations.map((recommendation, index) => (
              <tr key={index}>
                <td style={{ border: '1px solid black', textAlign: 'center' }}>
                  <a href={recommendation.track_link} target="_blank" rel="noopener noreferrer">
                    <img src={recommendation.image} alt="Album" style={{ width: '100px', height: '100px' }} />
                  </a>
                </td>
                <td style={{ border: '1px solid black', paddingLeft: '10px' }}>
                  <div>
                    <div style={{ color: 'black', fontWeight: 'bold', fontSize: '1.2rem' }}>{recommendation.track_name}</div>
                    <div style={{ color: 'dark-gray', fontSize: '0.8rem', paddingLeft: '5px' }}>{recommendation.artist_name}</div>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Home;
