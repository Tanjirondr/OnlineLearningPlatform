import React, { useEffect, useState } from 'react';

interface ICourse {
  id: number;
  name: string;
  description: string;
}

const CourseItem: React.FC<ICourse> = ({ id, name, description }) => (
  <li key={id}>
    {name}: {description}
  </li>
);

const CoursesList: React.FC = () => {
  const [courses, setCourses] = useState<ICourse[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchCourses = async () => {
    const backendUrl = process.env.REACT_APP_BACKEND_URL;
    if (!backendUrl) {
      console.error("REACT_APP_BACKEND_URL is not defined.");
      setIsLoading(false);
      return;
    }

    const url = `${backendUrl}/courses`;
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Error fetching courses: ${response.statusText}`);
      }
      const data: ICourse[] = await response.json();
      setCourses(data);
    } catch (error) {
      console.error("Failed to fetch courses", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCourses();
  }, []);

  if (isLoading) {
    return <p>Loading courses...</p>;
  }

  if (courses.length === 0) {
    return <p>No courses available.</p>;
  }

  return (
    <ul>
      {courses.map(course => (
        <CourseItem key={course.id} {...course} />
      ))}
    </ul>
  );
};

export default CoursesList;