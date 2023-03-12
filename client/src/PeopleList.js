import { gql, useQuery } from '@apollo/client';
import React from 'react';

const GET_PEOPLE = gql`
  query {
    allPeople {
      name
      height
      mass
      gender
      homeworld

    }
  }
`;

function PeopleList(){

  const { loading, error, data } = useQuery(GET_PEOPLE);
  if (loading) return <p> loading ...</p>
  if (error) return <p> {error.message} </p>
  return (
    <div>
      <h1>Star Wars Characters</h1>
      <ul>
        {data.allPeople.map(person => (
          <li key={person.name}>
            <h2>{person.name}</h2>
            <p>Height: {person.height}</p>
            <p>Mass: {person.mass}</p>
            <p>Gender: {person.gender}</p>
            <p>homeworld: {person.homeworld}</p>
          </li>
        ))}
      </ul>
    </div>
  );

}

export default PeopleList;