import React, { useState } from "react";
import ancestorService from "../service/ancestorService.js";
import {toSnakeCase} from "../util/FamilyTreeUtil.jsx";

function AncestorForm() {
  const [error, setError] = useState('');
  const [husband, setHusband] = useState({
    firstName: '',
    lastName: '',
    nickName: '',
    dateOfBirth: '',
    dateOfDeath: '',
    gender: 'Male',
    location: '',
    occupation: ''
  });

  const [wife, setWife] = useState([
    {
      firstName: '',
      lastName: '',
      nickName: '',
      dateOfBirth: '',
      dateOfDeath: '',
      gender: 'Female',
      location: '',
      occupation: '',
      weddingDate: ''
    }
  ]);

    const handleHusbandChange = (e) => {
        setHusband({ ...husband, [e.target.name]: e.target.value });
    };

    const handleWifeChange = (index, e) => {
        const { name, value } = e.target;
        setWife((prevWives) =>
            prevWives.map((wife, i) =>
                i === index ? { ...wife, [name]: value } : wife
            )
        );
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
            if (!husband.firstName.trim() || !husband.lastName.trim()
            || wife.some((wife) => !wife.firstName.trim() || !wife.lastName.trim())) {
        setError('Please enter all the details');
        return;
    }

    setError('');
        const formattedData = toSnakeCase({ husband, wife: wife });
        console.log("Formatted Data:", JSON.stringify(formattedData, null, 2));

        try {
            const response = await ancestorService.addAncestor(formattedData);
            console.log('Ancestor added successfully:', response);
        } catch (error) {
            console.error('Failed to add ancestor:', error);
        }
    };

    const addWife = () => {
    setWife((prevWives) => [
      ...prevWives,
      { firstName: '', lastName: '', nickName: '', gender: 'Female', dateOfBirth: '', dateOfDeath: '', location: '', occupation: '' }
    ]);
  };

    return (
        <div>
            <h2>Enter Ancestor Details</h2>
            <form onSubmit={handleSubmit}>
                <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: '10px'}}>
                    <h3 style={{marginTop: '-10px', marginBottom: '5px'}}>Husband:</h3>
                    <div style={{display: 'flex', alignItems: 'center', marginBottom: '10px'}}>
                        <label style={{marginRight: '10px'}}>First Name:</label>
                        <input
                            type="text"
                            placeholder="First Name"
                            name="firstName"
                            value={husband.firstName}
                            onChange={handleHusbandChange}
                            style={{padding: '2px', fontSize: '12px', marginRight: '5px'}}
                        />
                    </div>
                    <div style={{display: 'flex', alignItems: 'center', marginBottom: '10px'}}>
                        <label style={{marginRight: '10px'}}>Last Name:</label>
                        <input
                            type="text"
                            placeholder="Last Name"
                            name="lastName"
                            value={husband.lastName}
                            onChange={handleHusbandChange}
                            style={{padding: '2px', fontSize: '12px', marginRight: '5px'}}
                        />
                    </div>
                    <div style={{display: 'flex', alignItems: 'center', marginBottom: '10px'}}>
                        <label style={{marginRight: '10px'}}>Nick Name:</label>
                        <input
                            type="text"
                            placeholder="Nick Name"
                            name="nickName"
                            value={husband.nickName}
                            onChange={handleHusbandChange}
                            style={{padding: '2px', fontSize: '12px', marginRight: '5px'}}
                        />
                    </div>
                    <div style={{display: 'flex', alignItems: 'center', marginBottom: '10px'}}>
                        <label style={{marginRight: '10px'}}>Date Of Birth:</label>
                        <input
                            type="date"
                            placeholder="Date Of Birth"
                            name="dateOfBirth"
                            value={husband.dateOfBirth}
                            onChange={handleHusbandChange}
                            style={{padding: '2px', fontSize: '12px', marginRight: '5px'}}
                        />
                    </div>
                    <div style={{display: 'flex', alignItems: 'center', marginBottom: '10px'}}>
                        <label style={{marginRight: '10px'}}>Date Of Death:</label>
                        <input
                            type="date"
                            placeholder="Date Of Death"
                            name="dateOfDeath"
                            value={husband.dateOfDeath}
                            onChange={handleHusbandChange}
                            style={{padding: '2px', fontSize: '12px', marginRight: '5px'}}
                        />
                    </div>
                    <div style={{display: 'flex', alignItems: 'center', marginBottom: '10px'}}>
                        <label style={{marginRight: '10px'}}>Gender:</label>
                        <select
                            name="gender"
                            value={husband.gender}
                            onChange={handleHusbandChange}
                            style={{padding: '2px', fontSize: '12px', marginRight: '5px'}}
                        >
                            <option value="">Select Gender</option>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                        </select>
                    </div>
                    <div style={{display: 'flex', alignItems: 'center', marginBottom: '10px'}}>
                        <label style={{marginRight: '10px'}}>Location:</label>
                        <input
                            type="text"
                            placeholder="Location"
                            name="location"
                            value={husband.location}
                            onChange={handleHusbandChange}
                            style={{padding: '2px', fontSize: '12px', marginRight: '5px'}}
                        />
                    </div>
                    <div style={{display: 'flex', alignItems: 'center', marginBottom: '10px'}}>
                        <label style={{marginRight: '10px'}}>Occupation:</label>
                        <input
                            type="text"
                            placeholder="Occupation"
                            name="occupation"
                            value={husband.occupation}
                            onChange={handleHusbandChange}
                            style={{padding: '2px', fontSize: '12px', marginRight: '5px'}}
                        />
                    </div>
                </div>

                <div>
                    {wife.map((wife, index) => (
                        <div key={index} style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
                            <h3 style={{marginTop: '10px', marginBottom: '5px'}}>
                                {index === 0 ? 'Wife' : `Wife ${index + 1}`}
                            </h3>

                            <div style={{display: 'flex', alignItems: 'center', marginBottom: '10px'}}>
                                <label style={{marginRight: '10px'}}>First Name:</label>
                                <input
                                    type="text"
                                    placeholder="First Name"
                                    name="firstName"
                                    value={wife.firstName}
                                    onChange={(e) => handleWifeChange(index, e)}
                                    style={{padding: '2px', fontSize: '12px', marginRight: '5px'}}
                                />
                            </div>
                            <div style={{display: 'flex', alignItems: 'center', marginBottom: '10px'}}>
                                <label style={{marginRight: '10px'}}>Last Name:</label>
                                <input
                                    type="text"
                                    placeholder="Last Name"
                                    name="lastName"
                                    value={wife.lastName}
                                    onChange={(e) => handleWifeChange(index, e)}
                                    style={{padding: '2px', fontSize: '12px', marginRight: '5px'}}
                                />
                            </div>
                            <div style={{display: 'flex', alignItems: 'center', marginBottom: '10px'}}>
                                <label style={{marginRight: '10px'}}>Nick Name:</label>
                                <input
                                    type="text"
                                    placeholder="Nick Name"
                                    name="nickName"
                                    value={wife.nickName}
                                    onChange={(e) => handleWifeChange(index, e)}
                                    style={{padding: '2px', fontSize: '12px', marginRight: '5px'}}
                                />
                            </div>
                            <div style={{display: 'flex', alignItems: 'center', marginBottom: '10px'}}>
                                <label style={{marginRight: '10px'}}>Date Of Birth:</label>
                                <input
                                    type="date"
                                    placeholder="Date Of Birth"
                                    name="dateOfBirth"
                                    value={wife.dateOfBirth}
                                    onChange={(e) => handleWifeChange(index, e)}
                                    style={{padding: '2px', fontSize: '12px', marginRight: '5px'}}
                                />
                            </div>
                            <div style={{display: 'flex', alignItems: 'center', marginBottom: '10px'}}>
                                <label style={{marginRight: '10px'}}>Date Of Death:</label>
                                <input
                                    type="date"
                                    placeholder="Date Of Death"
                                    name="dateOfDeath"
                                    value={wife.dateOfDeath}
                                    onChange={(e) => handleWifeChange(index, e)}
                                    style={{padding: '2px', fontSize: '12px', marginRight: '5px'}}
                                />
                            </div>
                            <div style={{display: 'flex', alignItems: 'center', marginBottom: '10px'}}>
                                <label style={{marginRight: '10px'}}>Gender:</label>
                                <select
                                    name="gender"
                                    value={wife.gender}
                                    onChange={(e) => handleWifeChange(index, e)}
                                    style={{padding: '2px', fontSize: '12px', marginRight: '5px'}}
                                >
                                    <option value="">Select Gender</option>
                                    <option value="Male">Male</option>
                                    <option value="Female">Female</option>
                                </select>
                            </div>
                            <div style={{display: 'flex', alignItems: 'center', marginBottom: '10px'}}>
                                <label style={{marginRight: '10px'}}>Location:</label>
                                <input
                                    type="text"
                                    placeholder="Location"
                                    name="location"
                                    value={wife.location}
                                    onChange={(e) => handleWifeChange(index, e)}
                                    style={{padding: '2px', fontSize: '12px', marginRight: '5px'}}
                                />
                            </div>
                            <div style={{display: 'flex', alignItems: 'center', marginBottom: '10px'}}>
                                <label style={{marginRight: '10px'}}>Occupation:</label>
                                <input
                                    type="text"
                                    placeholder="Occupation"
                                    name="occupation"
                                    value={wife.occupation}
                                    onChange={(e) => handleWifeChange(index, e)}
                                    style={{padding: '2px', fontSize: '12px', marginRight: '5px'}}
                                />
                            </div>
                            <div style={{display: 'flex', alignItems: 'center', marginBottom: '10px'}}>
                                <label style={{marginRight: '10px'}}>Wedding Date:</label>
                                <input
                                    type="date"
                                    placeholder="Wedding Date"
                                    name="weddingDate"
                                    value={wife.weddingDate}
                                    onChange={(e) => handleWifeChange(index, e)}
                                    style={{padding: '2px', fontSize: '12px', marginRight: '5px'}}
                                />
                            </div>
                        </div>
                    ))}
                    <div style={{marginTop: "10px", textAlign: "center"}}>
                        <button type="button" onClick={addWife} style={{padding: "5px", fontSize: "14px"}}>
                            Add another Wife
                        </button>
                    </div>
                </div>

                {error && <div style={{color: 'red', marginTop: '10px'}}>{error}</div>}

                <div style={{marginTop: "10px", textAlign: "center"}}>
                    <button type="submit" style={{padding: "5px", fontSize: "14px"}}>
                        Submit
                    </button>
                </div>
            </form>
        </div>
    );
}

export default AncestorForm;
