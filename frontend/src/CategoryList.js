import React, { Component} from 'react';

import CategoryService from  './CategoryService';

const categoryService = new CategoryService()

class CategoriesList extends Component {

    constructor(props) {
        super(props);
        this.state = {
            categories: [],
            nextPageURL: ''
        };
        this.nextPage = this.nextPage.bind(this);
        this.handleDelete = this.handleDelete.bind(this)
    }

    componentDidMount() {
        var self = this;
        categoryService.getCategories().then(function(result) {
            console.log()
            self.setState({'categories': result.results, 'nextPageURL': result.next})
        })
    }

    handleDelete(e, slug){
        var  self  =  this;
        categoryService.deleteCategory({slug :  slug}).then(()=>{
            var  newArr  =  self.state.categories.filter(function(obj) {
                return  obj.slug  !==  slug;
            });
            self.setState({categories:  newArr})
        });
    }
    nextPage(){
        var  self  =  this;
        categoryService.getCategoryByURL(this.state.nextPageURL).then((result) => {
            self.setState({ categories:  result.data})
        });
}


    render() {

        return (
        <div  className="categories--list">
            <table  className="table">
                <thead  key="thead">
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Slug</th>
                </tr>
                </thead>
                <tbody>
                    {this.state.categories.map( c  =>
                    <tr  key={c.id}>
                        <td>{c.id}  </td>
                        <td>{c.name}</td>
                        <td>{c.slug}</td>
                        <td>
                        <button  onClick={(e)=>  this.handleDelete(e, c.slug) }> Delete</button>
                        <a  href={"/categories/" + c.slug}> Update</a>
                        </td>
                    </tr>)}
                </tbody>
            </table>
            <button  className="btn btn-primary"  onClick=  {  this.nextPage  }>Next</button>
        </div>
        );
    }
}

export default CategoriesList;
