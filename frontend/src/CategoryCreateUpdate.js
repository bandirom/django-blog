import React, { Component } from  'react';

import CategoryService from  './CategoryService';

const categoryService = new CategoryService()



class  CategoryCreateUpdate  extends  Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);

    }

    componentDidMount(){
        const { match: { params } } =  this.props;
        if(params  &&  params.slug)
        {
            categoryService.getCategory(params.slug).then((c)=>{
                this.refs.name.value  =  c.name;
            })
        }
    }

    handleSubmit(event) {
        const { match: { params } } =  this.props;
        if(params  &&  params.slug){
            this.handleUpdate(params.slug);
        }
        else
        {
            this.handleCreate();
        }
        event.preventDefault();
    }

    handleCreate(){
        categoryService.createCategory(
            {

            "name":  this.refs.name.value
            }).then((result)=>{
                    alert("Category created!");
            }).catch(()=>{
                    alert('There was an error! Please re-check your form.');
            });
    }

    handleUpdate(pk){
        categoryService.updateCategory(
            {
            "pk":  pk,
            "name":  this.refs.name.value,
            }
            ).then((result)=>{
        
                alert("Category updated!");
            }).catch(()=>{
                alert('There was an error! Please re-check your form.');
            });
        }

    render() {
        return (
          <form onSubmit={this.handleSubmit}>
          <div className="form-group">
    
            <label>Name:</label>
            <input className="form-control" type="text" ref='name'/>
            <input className="btn btn-primary" type="submit" value="Submit" />
            </div>
          </form>
        );
  }
}


export default CategoryCreateUpdate;