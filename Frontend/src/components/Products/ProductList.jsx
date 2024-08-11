import React, { useState, useEffect } from 'react';
import axios from 'axios';
import AsyncSelect from 'react-select/async';
import ProductForm from './ProductForm';
import { baseUrl } from '../../utils/constants/Constants';
import Swal from 'sweetalert2';

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const [showExpiredOnly, setShowExpiredOnly] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [totalQuantity, setTotalQuantity] = useState(null);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await axios.get(baseUrl + 'store/products/');
      setProducts(response.data.results);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };

  const loadProductIds = async (inputValue) => {
    if (!inputValue) return [];
    const response = await axios.get(`${baseUrl}store/products/search_codes/?query=${inputValue}`);
    return response.data.map(product => ({ label: product.product_code, value: product.product_code }));
  };

  const handleProductIdChange = async (selectedOption) => {
    if (!selectedOption) {
      setSelectedProduct(null);
      setTotalQuantity(null);
      return;
    }

    const productCode = selectedOption.value;
    setSelectedProduct(productCode);

    // Fetch total quantity for the selected product code
    try {
      const response = await axios.get(`${baseUrl}store/products/${productCode}/total_stock/`);
      setTotalQuantity(response.data.total_stock);
    } catch (error) {
      console.error('Error fetching total quantity:', error);
      setTotalQuantity(null);
    }
  };

  const deleteProduct = async (productCode) => {
    try {
      const result = await Swal.fire({
        title: 'Are you sure?',
        text: 'Do you want to delete this product?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'Cancel',
      });

      if (result.isConfirmed) {
        await axios.delete(`${baseUrl}store/products/${productCode}/`);
        Swal.fire('Deleted!', 'Your product has been deleted.', 'success');
        fetchProducts();
      }
    } catch (error) {
      console.error('Error deleting product:', error);
      Swal.fire('Error!', 'Failed to delete the product.', 'error');
    }
  };

  const editProduct = (product) => {
    setEditingProduct(product);
    setShowModal(true);
  };

  const filterExpiredProducts = () => {
    setShowExpiredOnly(!showExpiredOnly);
  };

  const filteredProducts = showExpiredOnly
    ? products.filter(product => new Date(product.expiry_date) < new Date())
    : products;

  return (
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center py-4">
        <h2 className="text-2xl font-bold">Products</h2>
        <div className="flex space-x-4">
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            onClick={() => {
              setEditingProduct(null);
              setShowModal(true);
            }}
          >
            Add Stock / Create Product
          </button>
          <button
            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
            onClick={filterExpiredProducts}
          >
            {showExpiredOnly ? 'Show All Products' : 'Show Expired Products'}
          </button>
        </div>
      </div>

      {/* Search bar for product ID */}
      <div className="my-4">
        <AsyncSelect
          loadOptions={loadProductIds}
          onChange={handleProductIdChange}
          isClearable
          placeholder="Search by Product ID..."
          className="w-full"
        />
      </div>

      {filteredProducts.length > 0 ? (
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white shadow-md rounded">
            <thead className="bg-gray-200 text-gray-600 uppercase text-sm leading-normal">
              <tr>
                <th className="py-3 px-6 text-left">Product Code</th>
                <th className="py-3 px-6 text-left">Name</th>
                <th className="py-3 px-6 text-left">Barcode</th>
                <th className="py-3 px-6 text-left">Category</th>
                <th className="py-3 px-6 text-left">Brand</th>
                <th className="py-3 px-6 text-left">Supplier</th>
                <th className="py-3 px-6 text-left">Purchase Date</th>
                <th className="py-3 px-6 text-left">Manufacturing Date</th>
                <th className="py-3 px-6 text-left">Expiry Date</th>
                <th className="py-3 px-6 text-left">Quantity</th>
                <th className="py-3 px-6 text-center">Actions</th>
              </tr>
            </thead>
            <tbody className="text-gray-600 text-sm">
              {filteredProducts.map((product) => {
                const stockClass =
                  product.total_stock === 0
                    ? 'bg-red-100'
                    : product.total_stock < 10
                    ? 'bg-yellow-100'
                    : '';

                return (
                  <tr
                    key={product.product_code}
                    className={`border-b border-gray-200 hover:bg-gray-100 ${stockClass}`}
                  >
                    <td className="py-3 px-6 text-left">{product.product_code}</td>
                    <td className="py-3 px-6 text-left">{product.name}</td>
                    <td className="py-3 px-6 text-left">{product.barcode}</td>
                    <td className="py-3 px-6 text-left">{product.category_name}</td>
                    <td className="py-3 px-6 text-left">{product.brand_name}</td>
                    <td className="py-3 px-6 text-left">{product.supplier_name}</td>
                    <td className="py-3 px-6 text-left">{product.purchase_date}</td>
                    <td className="py-3 px-6 text-left">{product.manufacturing_date}</td>
                    <td className="py-3 px-6 text-left">{product.expiry_date}</td>
                    <td className="py-3 px-6 text-left">{product.quantity}</td>
                    <td className="py-3 px-6 text-center space-x-2">
                      <button
                        className="bg-yellow-500 text-white px-4 py-2 mb-2 rounded hover:bg-yellow-600"
                        onClick={() => editProduct(product)}
                      >
                        Edit
                      </button>
                      <button
                        className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                        onClick={() => deleteProduct(product.product_code)}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="text-center py-8 text-gray-500">
          No products available. Add stock or create a new product to get started.
        </div>
      )}

      {/* Display total quantity for selected product ID in a decorative box */}
      {selectedProduct && totalQuantity !== null && (
        <div className="mt-4 bg-gradient-to-r from-blue-400 to-blue-600 p-6 rounded-lg shadow-lg text-white">
          <h3 className="text-xl font-bold mb-2">Total Quantity</h3>
          <p className="text-3xl font-extrabold">{totalQuantity}</p>
          <p className="mt-2 text-sm">Product ID: {selectedProduct}</p>
        </div>
      )}

      {showModal && (
        <ProductForm
          setShowModal={setShowModal}
          fetchProducts={fetchProducts}
          editingProduct={editingProduct}
        />
      )}
    </div>
  );
};

export default ProductList;
