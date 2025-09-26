import { useState, useEffect } from 'react';
import axios from 'axios';
import Link from 'next/link';

// Use environment variable for the API base URL
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Home() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchBooks = async () => {
    try {
  const response = await axios.get(`${API_URL}/api/v1/books/`);
      setBooks(response.data);
    } catch (error) {
      console.error('Error fetching books:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBooks();
  }, []);

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this book?')) {
      try {
  await axios.delete(`${API_URL}/api/v1/books/${id}`);
        // Refresh the list after successful deletion
        fetchBooks();
      } catch (error) {
        console.error('Error deleting book:', error);
        alert('Failed to delete book.');
      }
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '20px' }}>
      <h1>Book Catalog</h1>
      <Link href="/add">
        <button style={{ padding: '10px 15px', marginBottom: '20px' }}>Add New Book</button>
      </Link>

      {books.length === 0 ? (
        <p>No books found. Add one!</p>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid #ccc' }}>
              <th style={{ padding: '10px', textAlign: 'left' }}>Title</th>
              <th style={{ padding: '10px', textAlign: 'left' }}>Author</th>
              <th style={{ padding: '10px', textAlign: 'left' }}>Year</th>
              <th style={{ padding: '10px', textAlign: 'left' }}>ISBN</th>
              <th style={{ padding: '10px', textAlign: 'left' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {books.map((book) => (
              <tr key={book.id} style={{ borderBottom: '1px solid #eee' }}>
                <td style={{ padding: '10px' }}>{book.title}</td>
                <td style={{ padding: '10px' }}>{book.author}</td>
                <td style={{ padding: '10px' }}>{book.publication_year || 'N/A'}</td>
                <td style={{ padding: '10px' }}>{book.isbn || 'N/A'}</td>
                <td style={{ padding: '10px' }}>
                  <Link href={`/edit/${book.id}`}>
                    <button style={{ marginRight: '10px' }}>Edit</button>
                  </Link>
                  <button onClick={() => handleDelete(book.id)} style={{ color: 'red' }}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}