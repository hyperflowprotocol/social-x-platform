import React, { useEffect } from 'react';
import { usePrivy } from '@privy-io/react-auth';
import { useNavigate } from 'react-router-dom';

const PrivyCallback = () => {
  const { ready, getAccessToken, user } = usePrivy();
  const navigate = useNavigate();

  useEffect(() => {
    const handleCallback = async () => {
      console.log('🚨 PRIVY CALLBACK: Processing OAuth callback...');
      
      if (!ready) {
        console.log('Privy not ready yet, waiting...');
        return;
      }

      try {
        // Force session sync
        console.log('Syncing session...');
        await getAccessToken();
        
        // Poll for updated user data with Twitter account
        let attempts = 0;
        const maxAttempts = 16; // ~5 seconds
        
        const pollForTwitter = () => {
          const twitterLinked = user?.linkedAccounts?.find(account => 
            (account?.type === 'oauth' && ['twitter', 'x'].includes(account?.provider)) ||
            ['twitter', 'twitter_oauth', 'oauth_twitter'].includes(account?.type)
          ) || user?.twitter;
          
          console.log(`Poll attempt ${attempts + 1}: Twitter linked =`, !!twitterLinked);
          
          if (twitterLinked || attempts >= maxAttempts) {
            console.log('✅ User data synced! Navigating back...');
            // Use window.location.replace for reliable state refresh
            window.location.replace('/launch');
          } else {
            attempts++;
            setTimeout(pollForTwitter, 300);
          }
        };
        
        // Start polling
        setTimeout(pollForTwitter, 500);
        
      } catch (error) {
        console.error('Failed to sync session after OAuth:', error);
        // Fallback: force reload anyway
        setTimeout(() => {
          window.location.replace('/launch');
        }, 2000);
      }
    };

    handleCallback();
  }, [ready, getAccessToken, user]);

  return (
    <div style={{
      height: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: '#ffffff',
      color: '#000000'
    }}>
      <div style={{ textAlign: 'center' }}>
        <div style={{ 
          fontSize: '48px', 
          marginBottom: '20px',
          animation: 'spin 1s linear infinite' 
        }}>
          🔄
        </div>
        <h2 style={{ color: '#000000' }}>Connecting your X account...</h2>
        <p style={{ color: '#000000' }}>Please wait while we sync your profile data.</p>
      </div>
      <style jsx>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default PrivyCallback;