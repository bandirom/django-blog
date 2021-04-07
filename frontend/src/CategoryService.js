import axios from 'axios';
const API_URL = 'http://localhost:8008';

export default class CategoryService{

  constructor(){}

  getCategories(){
    const url = `${API_URL}/categories/`;
    return axios.get(url).then(response => response.data);

  }
  getCategory(slug) {
    const url = `${API_URL}/categories/${slug}/`;
    return axios.get(url).then(response => response.data);
  }
  getCategoryByURL(link){
    const url = `${API_URL}${link}`;
    return axios.get(url).then(response => response.data);
}
  deleteCategory(slug) {
    console.log(slug)
    const url = `${API_URL}/categories/${slug.slug}/`;
    return axios.delete(url)
  }
  createCustomer(data){
      const url = `${API_URL}/categories/`;
      return axios.post(url,data);
  }
  updateCustomer(category){
      const url = `${API_URL}/api/customers/${category.slug}`;
      return axios.put(url,category);
  }


}
