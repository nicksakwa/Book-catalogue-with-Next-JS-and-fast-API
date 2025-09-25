import BookForm from '../components/BookForm';

export default function AddBookPage() {
  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h1>Add New Book</h1>
      <BookForm />
    </div>
  );
}