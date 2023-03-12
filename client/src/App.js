import { ApolloProvider } from '@apollo/client';

import React from 'react';
import client from './graphql';
import PeopleList from './PeopleList';


function App() {
  return (
    <ApolloProvider client={client}>
      <div>
        <h1>My Blog</h1>
        <PeopleList />
      </div>
    </ApolloProvider>
  );
}

export default App;