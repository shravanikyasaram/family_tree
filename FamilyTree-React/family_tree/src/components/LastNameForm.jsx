import React, { useState } from 'react';

function LastNameForm({ onSubmit }) {
  const [lastName, setLastName] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!lastName.trim()) {
      setError('Please enter a Last Name');
      return;
    }
    onSubmit(lastName);
  };

  return (
    <div>
      <h2>Enter Last Name</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter last name"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
          style={{ padding: '10px', fontSize: '16px' }}
        />
        {error && <div style={{ color: 'red', marginTop: '10px' }}>{error}</div>}
        <button type="submit" style={{ padding: '10px', fontSize: '14px', marginLeft: '10px' }}>
          Submit
        </button>
      </form>
    </div>
  );
}

export default LastNameForm;
