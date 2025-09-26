import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const BookForm = ({ initialData = {}, isEdit = false }) => {
  const router = useRouter();
  const [formData, setFormData] = useState({
    title: '',
    author: '',
    publication_year: '',
    isbn: '',
    ...initialData,
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Populate form if initialData changes (only for edit)
    if (isEdit) {
        setFormData({
            ...initialData,
            // Ensure year is string for input value
            publication_year: initialData.publication_year || '',
            isbn: initialData.isbn || '',
        });
    }
  }, [initialData, isEdit]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);

    // Prepare data: convert year to number or set to null if empty
    const dataToSend = {
      ...formData,
      publication_year: formData.publication_year ? parseInt(formData.publication_year, 10) : null,
      // Remove empty strings for optional fields in PUT requests
      isbn: formData.isbn || null
    };

    // Remove ID if present in ADD mode
    if (!isEdit && dataToSend.id) {
        delete dataToSend.id;
    }
    
    // Remove null/empty fields from a PUT request for partial update
    const finalData = isEdit
      ? Object.fromEntries(Object.entries(dataToSend).filter(([_, v]) => v !== null && v !== ''))
      : dataToSend;


    try {
      if (isEdit) {
        await axios.put(`${API_URL}/api/v1/books/${initialData.id}`, finalData);
        alert('Book updated successfully!');
      } else {
        await axios.post(`${API_URL}/api/v1/books/`, finalData);
        alert('Book added successfully!');
      }
      router.push('/'); // Redirect to home page
    } catch (err) {
      console.error('API Error:', err.response ? err.response.data : err.message);
      setError('An error occurred. Check console for details.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '15px' }}>
      <div>
        <label htmlFor="title">Title (Required):</label>
        <input
          type="text"
          id="title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          required
        />
      </div>

      <div>
        <label htmlFor="author">Author (Required):</label>
        <input
          type="text"
          id="author"
          name="author"
          value={formData.author}
          onChange={handleChange}
          required
        />
      </div>

      <div>
        <label htmlFor="publication_year">Publication Year (Optional):</label>
        <input
          type="number"
          id="publication_year"
          name="publication_year"
          value={formData.publication_year}
          onChange={handleChange}
          min="1000"
          max="2100"
        />
      </div>

      <div>
        <label htmlFor="isbn">ISBN (Optional, Max 13 Chars):</label>
        <input
          type="text"
          id="isbn"
          name="isbn"
          value={formData.isbn}
          onChange={handleChange}
          maxLength="13"
        />
      </div>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <button type="submit" disabled={submitting}>
        {submitting ? 'Submitting...' : isEdit ? 'Update Book' : 'Add Book'}
      </button>
      <button type="button" onClick={() => router.push('/')} disabled={submitting}>
        Cancel
      </button>
    </form>
  );
};

export default BookForm;