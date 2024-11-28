import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import CourseList from './CourseList';
import CourseDetail from './CourseDetail';

const App: React.FC = () => {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={CourseList} />
        <Route path="/course/:id" component={CourseDetail} />
        <Route render={() => <CourseList />} />
      </Switch>
    </Router>
  );
};

export default App;