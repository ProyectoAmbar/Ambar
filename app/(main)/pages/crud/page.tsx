/* eslint-disable @next/next/no-img-element */
'use client';
import { Button } from 'primereact/button';
import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { Dialog } from 'primereact/dialog';
import { FileUpload } from 'primereact/fileupload';
import { InputNumber, InputNumberValueChangeEvent } from 'primereact/inputnumber';
import { InputText } from 'primereact/inputtext';
import { InputTextarea } from 'primereact/inputtextarea';
import { RadioButton, RadioButtonChangeEvent } from 'primereact/radiobutton';
import { Toast } from 'primereact/toast';
import { Toolbar } from 'primereact/toolbar';
import { classNames } from 'primereact/utils';
import React, { useEffect, useRef, useState } from 'react';
import { Demo } from '../../../../types/types';
import { getProducts, saveProductService, deleteProductService, updateProductService } from '../../../api/formServices';
import { Checkbox } from 'primereact/checkbox';
import S3Client from '../../../api/s3Client';

/* @todo Used 'as any' for types here. Will fix in next version due to onSelectionChange event type issue. */
const Crud = () => {
    let emptyProduct: Demo.ProductAmbar = {
        _id: '',
        nombre: '',
        imagenProducto: '',
        color: '',
        disponible: true,
        referencia: 0
    };

    const [products, setProducts] = useState(null);
    const [productDialog, setProductDialog] = useState(false);
    const [deleteProductDialog, setDeleteProductDialog] = useState(false);
    const [deleteProductsDialog, setDeleteProductsDialog] = useState(false);
    const [product, setProduct] = useState<Demo.ProductAmbar>(emptyProduct);
    const [selectedProducts, setSelectedProducts] = useState(null);
    const [submitted, setSubmitted] = useState(false);
    const [globalFilter, setGlobalFilter] = useState('');
    const toast = useRef<Toast>(null);
    const dt = useRef<DataTable<any>>(null);

    const loadProducts = async () => {
        try {
            const data = await getProducts();
            setProducts(data);
        } catch (error) {
            console.error('Error al cargar productos:', error);
        }
    };

    useEffect(() => {
        loadProducts();
    }, []);
    const openNew = () => {
        setProduct(emptyProduct);
        setSubmitted(false);
        setProductDialog(true);
    };

    const hideDialog = () => {
        setSubmitted(false);
        setProductDialog(false);
    };

    const hideDeleteProductDialog = () => {
        setDeleteProductDialog(false);
    };

    const hideDeleteProductsDialog = () => {
        setDeleteProductsDialog(false);
    };

    const uploadImageToS3 = async (file) => {
        const fileName = `${Date.now()}-${file.name}`;
        const params = {
            Bucket: 'ambar',
            Key: fileName,
            Body: file,
            ACL: 'public-read',
            ContentType: file.type
        };

        // try {
        //     const { Location } = await S3Client.upload(params).promise();
        //     return Location;
        // } catch (error) {
        //     console.error('Error al subir imagen a S3:', error);
        //     throw new Error('Error al subir imagen a S3');
        // }

        try {
            await S3Client.upload(params).promise();
            const publicUrl = `https://usc1.contabostorage.com/5c79aa9fa2cf480a98b39361fe8831a3:ambar/${fileName}`;
            return publicUrl;
        } catch (error) {
            console.error('Error al subir imagen a S3:', error);
            throw new Error('Error al subir imagen a S3');
        }
    };

    const onUploadHandler = async (e) => {
        if (e.files && e.files.length > 0) {
            const file = e.files[0];
            const maxSize = 1 * 1024 * 1024;

            if (file.size > maxSize) {
                toast.current?.show({
                    severity: 'error',
                    summary: 'Error',
                    detail: 'El archivo es demasiado grande. Tamaño máximo permitido: 1MB',
                    life: 3000
                });
                return;
            }

            try {
                const imageUrl = await uploadImageToS3(file);
                setProduct((prevProduct) => ({ ...prevProduct, imagenProducto: imageUrl }));
            } catch (error) {
                toast.current?.show({
                    severity: 'error',
                    summary: 'Error al subir imagen',
                    detail: error.message,
                    life: 3000
                });
            }
        } else {
            console.log('No se han cargado archivos.');
        }
    };

    const saveProduct = async () => {
        setSubmitted(true);
        const { _id, ...productData } = product;

        const referenciaExiste = products.some((prod) => prod.referencia === productData.referencia && prod._id !== _id);
        if (referenciaExiste) {
            toast.current?.show({
                severity: 'error',
                summary: 'Error',
                detail: 'Ya existe un producto con esa referencia.',
                life: 3000
            });
            return;
        }
        const nombreExiste = products.some((prod) => prod.nombre.toLowerCase() === productData.nombre.trim().toLowerCase() && prod._id !== _id);
        if (nombreExiste) {
            toast.current?.show({
                severity: 'error',
                summary: 'Error',
                detail: 'Ya existe un producto con ese nombre.',
                life: 3000
            });
            return;
        }

        if (productData.nombre.trim()) {
            try {
                if (_id) {
                    await updateProductService(_id, productData);
                } else {
                    await saveProductService(productData);
                }

                toast.current?.show({
                    severity: 'success',
                    summary: 'Éxito',
                    detail: _id ? 'Producto actualizado con éxito' : 'Producto creado con éxito',
                    life: 3000
                });

                await loadProducts();
                setProductDialog(false);
                setProduct(emptyProduct);
            } catch (error) {
                console.error('Error al guardar el producto:', error);
                toast.current?.show({
                    severity: 'error',
                    summary: 'Error',
                    detail: 'Error al guardar el producto',
                    life: 3000
                });
            }
        } else {
            toast.current?.show({
                severity: 'error',
                summary: 'Error',
                detail: 'El nombre del producto es obligatorio',
                life: 3000
            });
        }
    };

    const editProduct = (product: Demo.ProductAmbar) => {
        setProduct({ ...product });
        setProductDialog(true);
    };

    const confirmDeleteProduct = (product: Demo.ProductAmbar) => {
        setProduct(product);
        setDeleteProductDialog(true);
    };

    const deleteProduct = async () => {
        if (product._id) {
            try {
                await deleteProductService(product._id);
                toast.current?.show({
                    severity: 'success',
                    summary: 'Successful',
                    detail: 'Product Deleted',
                    life: 3000
                });
                await loadProducts();
            } catch (error) {
                console.error('Error al eliminar el producto:', error);
                toast.current?.show({
                    severity: 'error',
                    summary: 'Error',
                    detail: 'Error al eliminar el producto',
                    life: 3000
                });
            }
        }
        setDeleteProductDialog(false);
        setProduct(emptyProduct);
    };

    const exportCSV = () => {
        dt.current?.exportCSV();
    };

    const confirmDeleteSelected = () => {
        setDeleteProductsDialog(true);
    };

    const deleteSelectedProducts = () => {
        let _products = (products as any)?.filter((val: any) => !(selectedProducts as any)?.includes(val));
        setProducts(_products);
        setDeleteProductsDialog(false);
        setSelectedProducts(null);
        toast.current?.show({
            severity: 'success',
            summary: 'Successful',
            detail: 'Products Deleted',
            life: 3000
        });
    };

    const onInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>, nombre: string) => {
        const val = (e.target && e.target.value) || '';
        let _product = { ...product };
        _product[`${nombre}`] = val;

        setProduct(_product);
    };

    const onInputNumberChange = (e: InputNumberValueChangeEvent, name: string) => {
        const val = e.value || 0;
        let _product = { ...product };
        _product[`${name}`] = val;

        setProduct(_product);
    };

    const leftToolbarTemplate = () => {
        return (
            <React.Fragment>
                <div className="my-2 flex">
                    <Button label="Nuevo" icon="pi pi-plus" severity="success" className=" mr-2" onClick={openNew} />
                    <Button label="Eliminar" icon="pi pi-trash" severity="danger" onClick={confirmDeleteSelected} disabled={!selectedProducts || !(selectedProducts as any).length} />
                </div>
            </React.Fragment>
        );
    };

    const rightToolbarTemplate = () => {
        return (
            <React.Fragment>
                <FileUpload mode="basic" accept="image/*" maxFileSize={1000000} chooseLabel="Importar" className="mr-2 inline-block" />
                <Button label="Exportar" icon="pi pi-upload" severity="help" onClick={exportCSV} />
            </React.Fragment>
        );
    };

    const codeBodyTemplate = (rowData: Demo.ProductAmbar) => {
        return (
            <>
                <span className="p-column-title">Codigo </span>
                {rowData._id}
            </>
        );
    };

    const nameBodyTemplate = (rowData: Demo.ProductAmbar) => {
        return (
            <>
                <span className="p-column-title">Nombre</span>
                {rowData.nombre}
            </>
        );
    };

    const colorBodyTemplate = (rowData: Demo.ProductAmbar) => {
        return (
            <>
                <span className="p-column-title">Color</span>
                {rowData.color}
            </>
        );
    };
    const imageBodyTemplate = (rowData) => {
        return rowData.imagenProducto ? (
            <>
                <span className="p-column-title">Imagen</span>
                <img src={rowData.imagenProducto} alt={rowData.nombre} className="product-image" />
            </>
        ) : (
            <>
                <span className="p-column-title">Imagen</span>
                <span>No disponible</span>
            </>
        );
    };
    const referenceBodyTemplate = (rowData: Demo.ProductAmbar) => {
        return (
            <>
                <span className="p-column-title">Referencia</span>
                {rowData.referencia as number}
            </>
        );
    };

    const statusBodyTemplate = (rowData: Demo.ProductAmbar) => {
        const statusClass = rowData.disponible ? 'status-disponible' : 'status-outofstock';

        return (
            <>
                <span className="p-column-title">Estado</span>
                <span className={`product-badge ${statusClass}`}>{rowData.disponible ? 'Disponible' : 'No Disponible'}</span>
            </>
        );
    };

    const actionBodyTemplate = (rowData: Demo.ProductAmbar) => {
        return (
            <>
                <Button icon="pi pi-pencil" rounded severity="success" className="mr-2" onClick={() => editProduct(rowData)} />
                <Button icon="pi pi-trash" rounded severity="warning" onClick={() => confirmDeleteProduct(rowData)} />
            </>
        );
    };

    const header = (
        <div className="flex flex-column md:flex-row md:justify-content-between md:align-items-center">
            <h5 className="m-0">Gestionar Productos</h5>
            <span className="block mt-2 md:mt-0 p-input-icon-left">
                <i className="pi pi-search" />
                <InputText type="search" onInput={(e) => setGlobalFilter(e.currentTarget.value)} placeholder="Buscar Producto Por Nombre..." />
            </span>
        </div>
    );

    const productDialogFooter = (
        <>
            <Button label="Cancelar" icon="pi pi-times" text onClick={hideDialog} />
            <Button label="Guardar" icon="pi pi-check" text onClick={saveProduct} />
        </>
    );
    const deleteProductDialogFooter = (
        <>
            <Button label="No" icon="pi pi-times" text onClick={hideDeleteProductDialog} />
            <Button label="Si" icon="pi pi-check" text onClick={deleteProduct} />
        </>
    );
    const deleteProductsDialogFooter = (
        <>
            <Button label="No" icon="pi pi-times" text onClick={hideDeleteProductsDialog} />
            <Button label="Si" icon="pi pi-check" text onClick={deleteSelectedProducts} />
        </>
    );

    return (
        <div className="grid crud-demo">
            <div className="col-12">
                <div className="card">
                    <Toast ref={toast} />
                    <Toolbar className="mb-4" left={leftToolbarTemplate} right={rightToolbarTemplate}></Toolbar>

                    <DataTable
                        ref={dt}
                        value={products}
                        selection={selectedProducts}
                        onSelectionChange={(e) => setSelectedProducts(e.value as any)}
                        dataKey="_id"
                        paginator
                        rows={10}
                        rowsPerPageOptions={[5, 10, 25]}
                        className="datatable-responsive"
                        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                        currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} Productos"
                        globalFilter={globalFilter}
                        emptyMessage="Productos no Encontrados."
                        header={header}
                        responsiveLayout="scroll"
                    >
                        <Column selectionMode="multiple" headerStyle={{ width: '4rem' }}></Column>
                        <Column field="Codigo" header="Codigo" sortable body={codeBodyTemplate} headerStyle={{ minWidth: '15rem' }}></Column>
                        <Column field="nombre" header="Nombre" sortable body={nameBodyTemplate} headerStyle={{ minWidth: '15rem' }}></Column>
                        <Column field="color" header="Color" sortable body={colorBodyTemplate} headerStyle={{ minWidth: '15rem' }}></Column>
                        <Column header="Imagen" body={imageBodyTemplate}></Column>
                        <Column field="Referencia" header="Referencia" body={referenceBodyTemplate} sortable></Column>
                        <Column field="inventoryStatus" header="Estado" body={statusBodyTemplate} sortable headerStyle={{ minWidth: '10rem' }}></Column>
                        <Column body={actionBodyTemplate} headerStyle={{ minWidth: '10rem' }}></Column>
                    </DataTable>

                    {/* Modal para crear y editar Productos */}
                    <Dialog visible={productDialog} style={{ width: '450px' }} header="Detalles del Producto" modal className="p-fluid" footer={productDialogFooter} onHide={hideDialog}>
                        <div className="field">
                            <label htmlFor="image">Imagen (Máximo 1MB)</label>

                            {/* Muestra la imagen actual si existe */}
                            {product.imagenProducto && <img src={product.imagenProducto} alt="Imagen del producto" width="150" className="mb-2 block mx-auto" />}

                            {/* Componente FileUpload siempre disponible para cargar o cambiar la imagen */}
                            <FileUpload
                                mode="advanced"
                                name="demo[]"
                                accept="image/*"
                                maxFileSize={1000000}
                                chooseLabel={product.imagenProducto ? 'Cambiar imagen' : 'Seleccionar imagen'}
                                customUpload={true}
                                uploadHandler={onUploadHandler}
                                emptyTemplate={<p className="m-0">Arrastre y suelte la imagen aquí o haga clic para seleccionar. Tamaño máximo 1MB.</p>}
                            />
                        </div>

                        <div className="field">
                            <label htmlFor="nombre">Nombre</label>
                            <InputText id="nombre" value={product.nombre} onChange={(e) => onInputChange(e, 'nombre')} required autoFocus className={classNames({ 'p-invalid': submitted && !product.nombre })} />
                            {submitted && !product.nombre && <small className="p-invalid">Nombre es Obligatorio</small>}
                        </div>
                        <div className="field">
                            <label htmlFor="color">Color</label>
                            <InputText id="color" value={product.color} onChange={(e) => onInputChange(e, 'color')} required />
                        </div>
                        <div className="field">
                            <label htmlFor="referencia">Referencia</label>
                            <InputNumber id="referencia" value={product.referencia} onValueChange={(e) => onInputNumberChange(e, 'referencia')} mode="decimal" useGrouping={false} required />
                        </div>
                        <Checkbox inputId="disponible" checked={product.disponible} onChange={(e: any) => onInputChange(e, 'disponible')} />
                    </Dialog>

                    <Dialog visible={deleteProductDialog} style={{ width: '450px' }} header="Confirm" modal footer={deleteProductDialogFooter} onHide={hideDeleteProductDialog}>
                        <div className="flex align-items-center justify-content-center">
                            <i className="pi pi-exclamation-triangle mr-3" style={{ fontSize: '2rem' }} />
                            {product && (
                                <span>
                                    Estas seguro de eliminar este Producto? <b>{product.nombre}</b>?
                                </span>
                            )}
                        </div>
                    </Dialog>

                    <Dialog visible={deleteProductsDialog} style={{ width: '450px' }} header="Confirm" modal footer={deleteProductsDialogFooter} onHide={hideDeleteProductsDialog}>
                        <div className="flex align-items-center justify-content-center">
                            <i className="pi pi-exclamation-triangle mr-3" style={{ fontSize: '2rem' }} />
                            {product && <span>Estas seguro de eliminar estos Productos?</span>}
                        </div>
                    </Dialog>
                </div>
            </div>
        </div>
    );
};

export default Crud;
