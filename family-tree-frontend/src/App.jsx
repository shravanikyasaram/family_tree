import React, { useState } from 'react';

function App() {
  const [lastName, setLastName] = useState('');
  const [greeting, setGreeting] = useState('');
  const [error, setError] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);

  const [husband, setHusband] = useState({
    firstName: '',
    lastName: '',
    nickName: '',
    gender: 'Male',
    dateOfBirth: '',
    dateOfDeath: '',
    location: '',
    occupation: ''
  });

  const [wives, setWives] = useState([
    {
      firstName: '',
      lastName: '',
      nickName: '',
      gender: 'Female',
      dateOfBirth: '',
      dateOfDeath: '',
      location: '',
      occupation: ''
    }
  ]);

  const handleHusbandChange = (field, value) => {
    setHusband((prev) => ({ ...prev, [field]: value }));
  };

  const handleWifeChange = (index, field, value) => {
    setWives((prevWives) => {
      const updatedWives = [...prevWives];
      updatedWives[index][field] = value;
      return updatedWives;
    });
  };

  const addWife = () => {
    setWives((prevWives) => [
      ...prevWives,
      { firstName: '', lastName: '', nickName: '', gender: 'Female', dateOfBirth: '', dateOfDeath: '', location: '', occupation: '' }
    ]);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!lastName.trim()) {
      setError("Please enter a Last Name");
      return;
    }
    setGreeting(`Welcome to ${lastName.toUpperCase()}'s Family Tree!`);
    setIsSubmitted(true);
  };

  return (
    <div style={{ padding: '20px', textAlign: 'center', height: '100vh' }}>
      {/* Display "Enter Last Name" form only when not submitted */}
      {!isSubmitted && (
        <>
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
        </>
      )}

      {isSubmitted && (
        <>
          {/* Greeting message */}
          <h1 style={{ marginBottom: '20px' }}>{greeting}</h1>

          <div style={{ padding: '0px', marginTop: '20px' }}>
            <h2>Enter Ancestor Details</h2>

            {/* Husband details - Centered */}
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: '10px' }}>
              <h3 style={{ marginTop: '-10px', marginBottom: '10px' }}>Husband:</h3>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                <label style={{ marginRight: '10px' }}>First Name:</label>
                <input
                  type="text"
                  placeholder="First Name"
                  value={husband.firstName}
                  onChange={(e) => handleHusbandChange('firstName', e.target.value)}
                  style={{ padding: '5px', marginRight: '200px' }}
                />
              </div>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                <label style={{ marginRight: '10px' }}>Last Name:</label>
                <input
                  type="text"
                  placeholder="Last Name"
                  value={husband.lastName}
                  onChange={(e) => handleHusbandChange('lastName', e.target.value)}
                  style={{ padding: '5px', marginRight: '200px' }}
                />
              </div>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                <label style={{ marginRight: '10px' }}>Nick Name:</label>
                <input
                  type="text"
                  placeholder="Nick Name"
                  value={husband.nickName}
                  onChange={(e) => handleHusbandChange('nickName', e.target.value)}
                  style={{ padding: '5px', marginRight: '200px' }}
                />
              </div>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                <label style={{ marginRight: '10px' }}>Gender:</label>
                <select
                  value={husband.gender}
                  onChange={(e) => handleHusbandChange('gender', e.target.value)}
                  style={{ padding: '4px', marginRight: '200px' }}
                >
                  <option value="">Select Gender</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                </select>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                <label style={{ marginRight: '10px' }}>Date Of Birth:</label>
                <input
                  type="date"
                  placeholder="Date Of Birth"
                  value={husband.dateOfBirth}
                  onChange={(e) => handleHusbandChange('dateOfBirth', e.target.value)}
                  style={{ padding: '5px', marginRight: '200px' }}
                />
              </div>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                <label style={{ marginRight: '10px' }}>Date Of Death:</label>
                <input
                  type="date"
                  placeholder="Date Of Death"
                  value={husband.dateOfDeath}
                  onChange={(e) => handleHusbandChange('dateOfDeath', e.target.value)}
                  style={{ padding: '5px', marginRight: '200px' }}
                />
              </div>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                <label style={{ marginRight: '10px' }}>Location:</label>
                <input
                  type="text"
                  placeholder="Location"
                  value={husband.location}
                  onChange={(e) => handleHusbandChange('location', e.target.value)}
                  style={{ padding: '5px', marginRight: '200px' }}
                />
              </div>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                <label style={{ marginRight: '10px' }}>Occupation:</label>
                <input
                  type="text"
                  placeholder="Occupation"
                  value={husband.occupation}
                  onChange={(e) => handleHusbandChange('occupation', e.target.value)}
                  style={{ padding: '5px', marginRight: '200px' }}
                />
              </div>
            </div>

            {/* Wives details - Left aligned */}
            <div>
              {wives.map((wife, index) => (
                <div key={index} style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
                  <h3 style={{ marginTop: '10px', marginBottom: '10px' }}>
                    {index === 0 ? 'Wife' : `Wife ${index + 1}`}
                  </h3>

                  <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                    <label style={{ marginRight: '10px' }}>First Name:</label>
                    <input
                      type="text"
                      placeholder="First Name"
                      value={wife.firstName}
                      onChange={(e) => handleWifeChange(index, 'firstName', e.target.value)}
                      style={{ padding: '5px', marginRight: '200px' }}
                    />
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                    <label style={{ marginRight: '10px' }}>Last Name:</label>
                    <input
                      type="text"
                      placeholder="Last Name"
                      value={wife.lastName}
                      onChange={(e) => handleWifeChange(index, 'lastName', e.target.value)}
                      style={{ padding: '5px', marginRight: '200px' }}
                    />
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                    <label style={{ marginRight: '10px' }}>Nick Name:</label>
                    <input
                      type="text"
                      placeholder="Nick Name"
                      value={wife.nickName}
                      onChange={(e) => handleWifeChange(index, 'nickName', e.target.value)}
                      style={{ padding: '5px', marginRight: '200px' }}
                    />
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                    <label style={{ marginRight: '10px' }}>Gender:</label>
                    <select
                      value={wife.gender}
                      onChange={(e) => handleWifeChange(index, 'gender', e.target.value)}
                      style={{ padding: '4px', marginRight: '200px' }}
                    >
                      <option value="">Select Gender</option>
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                    </select>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                    <label style={{ marginRight: '10px' }}>Date Of Birth:</label>
                    <input
                      type="date"
                      placeholder="Date Of Birth"
                      value={wife.dateOfBirth}
                      onChange={(e) => handleWifeChange(index, 'dateOfBirth', e.target.value)}
                      style={{ padding: '5px', marginRight: '200px' }}
                    />
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                    <label style={{ marginRight: '10px' }}>Date Of Death:</label>
                    <input
                      type="date"
                      placeholder="Date Of Death"
                      value={wife.dateOfDeath}
                      onChange={(e) => handleWifeChange(index, 'dateOfDeath', e.target.value)}
                      style={{ padding: '5px', marginRight: '200px' }}
                    />
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                    <label style={{ marginRight: '10px' }}>Location:</label>
                    <input
                      type="text"
                      placeholder="Location"
                      value={wife.location}
                      onChange={(e) => handleWifeChange(index, 'location', e.target.value)}
                      style={{ padding: '5px', marginRight: '200px' }}
                    />
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                    <label style={{ marginRight: '10px' }}>Occupation:</label>
                    <input
                      type="text"
                      placeholder="Occupation"
                      value={wife.occupation}
                      onChange={(e) => handleWifeChange(index, 'occupation', e.target.value)}
                      style={{ padding: '5px', marginRight: '200px' }}
                    />
                  </div>
                </div>
              ))}
              <button type="button" onClick={addWife}>
                Add another Wife
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
