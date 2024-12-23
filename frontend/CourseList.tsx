import React, { useEffect, useState } from 'react';

interface ICourse {
  id: number;
  name: string;
  description: string;
}

const CoursesList: React.FC = () => {
  const [courses, setCourses] = useState<ICourse[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const fetchCourses = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/courses`);
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

  return (
    <div>
      {isLoading ? (
        <p>Loading courses...</p>
      ) : courses.length > 0 ? (
        <ul>
          {courses.map((course) => (
            <li key={course.id}>{course.name}: {course.description}</li>
          ))}
        </ul>
      ) : (
        <p>No courses available.</p>
      )}
    </div>
  );
};

export default CoursesList;