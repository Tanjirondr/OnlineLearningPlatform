import React from 'react';
import { BrowserRouter as AppRouter, Route, Switch } from 'react-router-dom';
import CourseListView from './CourseList';
import CourseDetailView from './CourseDetail';

const App: React.FC = () => {
  return (
    <AppRouter>
      <Switch>
        <Route exact path="/" component={CourseListView} />
        <Route path="/course/:id" component={CourseDetailView} />
        <Route render={() => <CourseListView />} />
      </Switch>
    </AppRouter>
  );
};

export default App;