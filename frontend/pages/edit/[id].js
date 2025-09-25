import { useRouter } from 'next/router';
import { useState, useEffect } from 'react';
import axios from 'axios';
import BookForm from '../../components/BookForm';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function EditBookPage() {
  const router = useRouter();
  const { id } = router.query;
  const [book, setBook] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      const fetchBook = async () => {
        try {
          const response = await axios.get(`${API_URL}/books/${id}`);
          setBook(response.data);
        } catch (error) {
          console.error('Error fetching book:', error);
          alert('Could not load book for editing.');
          router.push('/');
        } finally {
          setLoading(false);
        }
      };
      fetchBook();
    }
  }, [id, router]);

  if (loading || !book) return <div>Loading book data...</div>;

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h1>Edit Book: {book.title}</h1>
      <BookForm initialData={book} isEdit={true} />
    </div>
  );
}