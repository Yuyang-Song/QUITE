# 403 forbidden error in custom module in magento
[Link to question](https://stackoverflow.com/questions/35047307/403-forbidden-error-in-custom-module-in-magento)
**Creation Date:** 1453926248
**Score:** 0
**Tags:** magento-1.9.1
## Question Body
<p>I have custom module in magento, I am getting Forbidden error like below-</p>

<pre><code>Forbidden

You don't have permission to access /index.php/custom/adminhtml_custom/save/id/73/key/46af940903ec3251359c2b5db00e8092/back/edit/ on this server.
</code></pre>

<p>This problem is coming after clicking on Save or save and continue edit button.</p>

<p>Here is the controller file which have save function--</p>

<pre><code>&lt;?php
class Assel_Custom_Adminhtml_CustomController extends Mage_Adminhtml_Controller_Action
{

    protected function _initAction() {
        $this-&gt;loadLayout();
        return $this;
    }   

    public function indexAction() {
        $this-&gt;_initAction()
            -&gt;_addContent($this-&gt;getLayout()-&gt;createBlock('custom/adminhtml_custom'))
            -&gt;renderLayout();
    }

    public function editAction() {
        $id     = $this-&gt;getRequest()-&gt;getParam('id');
        $model  = Mage::getModel('custom/custom')-&gt;load($id);

        if ($model-&gt;getId() || $id == 0) {
            $data = Mage::getSingleton('adminhtml/session')-&gt;getFormData(true);
            if (!empty($data)) {
                $model-&gt;setData($data);
            }

            Mage::register('custom_data', $model);

            $this-&gt;loadLayout();
            $this-&gt;_setActiveMenu('custom/items');

            $this-&gt;_addBreadcrumb(Mage::helper('adminhtml')-&gt;__('Item Manager'), Mage::helper('adminhtml')-&gt;__('Item Manager'));
            $this-&gt;_addBreadcrumb(Mage::helper('adminhtml')-&gt;__('Item News'), Mage::helper('adminhtml')-&gt;__('Item News'));

            $this-&gt;getLayout()-&gt;getBlock('head')-&gt;setCanLoadExtJs(true);

            $this-&gt;_addContent($this-&gt;getLayout()-&gt;createBlock('custom/adminhtml_custom_edit'));

            $this-&gt;renderLayout();
        } else {
            Mage::getSingleton('adminhtml/session')-&gt;addError(Mage::helper('custom')-&gt;__('Item does not exist'));
            $this-&gt;_redirect('adminhtml/cms_page/edit/',array('page_id' =&gt; $this-&gt;getRequest()-&gt;getParam('page_id')));
        }
    }

    public function newAction() {
        $this-&gt;_forward('edit');
    }

    public function saveAction() 
    {
        $filedata = array();
        $main_image = 'main_image';

        $_helper = Mage::helper('custom');
        if (!empty($_FILES[$main_image]['name'])) {
            try {
                $ext = $_helper-&gt;getFileExtension($_FILES[$main_image]['name']);
                $fname = 'File-' . time() . $ext;
                $uploader = new Varien_File_Uploader($main_image);
                #$uploader-&gt;setAllowedExtensions(array("txt", "csv", "htm", "html", "xml", "css", "doc", "docx", "xls", "xlsx", "rtf", "ppt", "pdf", "swf", "flv", "avi", "wmv", "mov", "wav", "mp3", "jpg", "jpeg", "gif", "png","zip"));

                $uploader-&gt;setAllowRenameFiles(true);
                $uploader-&gt;setFilesDispersion(false);

                $path = Mage::getBaseDir('media') . DS . 'assel' . DS. 'custom' . DS;

                $uploader-&gt;save($path, $_FILES[$main_image]['name']);

                $filedata[$main_image] = 'assel/custom/' . $_FILES[$main_image]['name'];
            } catch (Exception $e) {
                Mage::getSingleton('adminhtml/session')-&gt;addError($e-&gt;getMessage());
                $this-&gt;_redirect('*/*/edit', array('page_id' =&gt; $this-&gt;getRequest()-&gt;getParam('page_id'),'id' =&gt; $this-&gt;getRequest()-&gt;getParam('id')));
                return;
            }
        }
        $backgrounddata = array();
        $background_image = 'background_image';
        if (!empty($_FILES[$background_image]['name'])) {
            try {
                $ext = $_helper-&gt;getFileExtension($_FILES[$background_image]['name']);
                $fname = 'File-' . time() . $ext;
                $uploader = new Varien_File_Uploader($background_image);
                #$uploader-&gt;setAllowedExtensions(array("txt", "csv", "htm", "html", "xml", "css", "doc", "docx", "xls", "xlsx", "rtf", "ppt", "pdf", "swf", "flv", "avi", "wmv", "mov", "wav", "mp3", "jpg", "jpeg", "gif", "png","zip"));

                $uploader-&gt;setAllowRenameFiles(true);
                $uploader-&gt;setFilesDispersion(false);

                $path = Mage::getBaseDir('media') . DS . 'assel' . DS. 'custom' . DS;

                $uploader-&gt;save($path, $_FILES[$background_image]['name']);

                $backgrounddata[$background_image] = 'assel/custom/' . $_FILES[$background_image]['name'];
            } catch (Exception $e) {
                Mage::getSingleton('adminhtml/session')-&gt;addError($e-&gt;getMessage());
                $this-&gt;_redirect('*/*/edit',array('page_id' =&gt; $this-&gt;getRequest()-&gt;getParam('page_id'),'id' =&gt; $this-&gt;getRequest()-&gt;getParam('id')));
                return;
            }
        }

        $thumbdata = array();
        $thumb_image = 'thumb_image';
        if (!empty($_FILES[$thumb_image]['name'])) {
            try {
                $ext = $_helper-&gt;getFileExtension($_FILES[$thumb_image]['name']);
                $fname = 'File-' . time() . $ext;
                $uploader = new Varien_File_Uploader($thumb_image);
                #$uploader-&gt;setAllowedExtensions(array("txt", "csv", "htm", "html", "xml", "css", "doc", "docx", "xls", "xlsx", "rtf", "ppt", "pdf", "swf", "flv", "avi", "wmv", "mov", "wav", "mp3", "jpg", "jpeg", "gif", "png","zip"));

                $uploader-&gt;setAllowRenameFiles(true);
                $uploader-&gt;setFilesDispersion(false);

                $path = Mage::getBaseDir('media') . DS . 'assel' . DS. 'custom' . DS;

                $uploader-&gt;save($path, $_FILES[$thumb_image]['name']);

                $thumbdata[$thumb_image] = 'assel/custom/' . $_FILES[$thumb_image]['name'];
            } catch (Exception $e) {
                Mage::getSingleton('adminhtml/session')-&gt;addError($e-&gt;getMessage());
                $this-&gt;_redirect('*/*/edit', array('page_id' =&gt; $this-&gt;getRequest()-&gt;getParam('page_id'),'id' =&gt; $this-&gt;getRequest()-&gt;getParam('id')));
                return;
            }
        }


        $circleimagedata = array();
        $circle_image = 'circle_image';
        if (!empty($_FILES[$circle_image]['name'])) {
            try {
                $ext = $_helper-&gt;getFileExtension($_FILES[$circle_image]['name']);
                $fname = 'File-' . time() . $ext;
                $uploader = new Varien_File_Uploader($circle_image);
                #$uploader-&gt;setAllowedExtensions(array("txt", "csv", "htm", "html", "xml", "css", "doc", "docx", "xls", "xlsx", "rtf", "ppt", "pdf", "swf", "flv", "avi", "wmv", "mov", "wav", "mp3", "jpg", "jpeg", "gif", "png","zip"));

                $uploader-&gt;setAllowRenameFiles(true);
                $uploader-&gt;setFilesDispersion(false);

                $path = Mage::getBaseDir('media') . DS . 'assel' . DS. 'custom' . DS;

                $uploader-&gt;save($path, $_FILES[$circle_image]['name']);

                $circleimagedata[$circle_image] = 'assel/custom/' . $_FILES[$circle_image]['name'];
            } catch (Exception $e) {
                Mage::getSingleton('adminhtml/session')-&gt;addError($e-&gt;getMessage());
                $this-&gt;_redirect('*/*/edit', array('page_id' =&gt; $this-&gt;getRequest()-&gt;getParam('page_id'),'id' =&gt; $this-&gt;getRequest()-&gt;getParam('id')));
                return;
            }
        }

        $audiodata = array();
        $audio_file = 'audio';
        if (!empty($_FILES[$audio_file]['name'])) {
            try {
                $ext = $_helper-&gt;getFileExtension($_FILES[$audio_file]['name']);
                $fname = 'File-' . time() . $ext;
                $uploader = new Varien_File_Uploader($audio_file);
                $uploader-&gt;setAllowedExtensions(array("wmv","mp3"));

                $uploader-&gt;setAllowRenameFiles(true);
                $uploader-&gt;setFilesDispersion(false);

                $path = Mage::getBaseDir('media') . DS . 'assel' . DS. 'custom' . DS;

                $uploader-&gt;save($path, $_FILES[$audio_file]['name']);

                $audiodata[$audio_file] = 'assel/custom/' . $_FILES[$audio_file]['name'];
            } catch (Exception $e) {
                Mage::getSingleton('adminhtml/session')-&gt;addError($e-&gt;getMessage());
                $this-&gt;_redirect('*/*/edit', array('page_id' =&gt; $this-&gt;getRequest()-&gt;getParam('page_id'),'id' =&gt; $this-&gt;getRequest()-&gt;getParam('id')));
                return;
            }
        }

        if ($data = $this-&gt;getRequest()-&gt;getPost()) {

            if (!empty($filedata[$main_image])) {
                $data[$main_image] = $filedata[$main_image];
            } else {
                if (isset($data[$main_image]['delete']) &amp;&amp; $data[$main_image]['delete'] == 1) {
                    if ($data[$main_image]['value'] != '')
                        $this-&gt;removeFile($data[$main_image]['value']);
                    $data[$main_image] = '';
                }else {
                    unset($data[$main_image]);
                }
            }

            if (!empty($backgrounddata[$background_image])) {
                $data[$background_image] = $backgrounddata[$background_image];
            } else {
                if (isset($data[$background_image]['delete']) &amp;&amp; $data[$background_image]['delete'] == 1) {
                    if ($data[$background_image]['value'] != '')
                        $this-&gt;removeFile($data[$background_image]['value']);
                    $data[$background_image] = '';
                }else {
                    unset($data[$background_image]);
                }
            }

            if (!empty($thumbdata[$thumb_image])) {
                $data[$thumb_image] = $thumbdata[$thumb_image];
            } else {
                if (isset($data[$thumb_image]['delete']) &amp;&amp; $data[$thumb_image]['delete'] == 1) {
                    if ($data[$thumb_image]['value'] != '')
                        $this-&gt;removeFile($data[$thumb_image]['value']);
                    $data[$thumb_image] = '';
                }else {
                    unset($data[$thumb_image]);
                }
            }

            if (!empty($circleimagedata[$circle_image])) {
                $data[$circle_image] = $circleimagedata[$circle_image];
            } else {
                if (isset($data[$circle_image]['delete']) &amp;&amp; $data[$circle_image]['delete'] == 1) {
                    if ($data[$circle_image]['value'] != '')
                        $this-&gt;removeFile($data[$circle_image]['value']);
                    $data[$circle_image] = '';
                }else {
                    unset($data[$circle_image]);
                }
            }

            if (!empty($audiodata[$audio_file])) {
                $data[$audio_file] = $audiodata[$audio_file];
            } else {
                if (isset($data[$audio_file]['delete']) &amp;&amp; $data[$audio_file]['delete'] == 1) {
                    if ($data[$audio_file]['value'] != '')
                        $this-&gt;removeFile($data[$audio_file]['value']);
                    $data[$audio_file] = '';
                }else {
                    unset($data[$audio_file]);
                }
            }

            if($data['block_type'] == 16)
            {
                $page_id=$this-&gt;getRequest()-&gt;getParam('page_id');
                $url= Mage::helper('cms/page')-&gt;getPageUrl($page_id);
                $char = Mage::getModel('character/character') -&gt; getCollection();
                $char-&gt;addFieldToFilter('name', $data['character']);
                foreach($char as $character)
                {
                    $id= $character-&gt;getData('id');
                }
                if($id)
                {
                    $char = Mage::getModel('character/character')-&gt;load($id);
                    $char-&gt;setLink($url)-&gt;save();
                }
            }

            foreach ($data as $key =&gt; $value)             /* save configurable product id in array in database*/
            {
                if (is_array($value))
                {
                    $data[$key] = implode(',',$this-&gt;getRequest()-&gt;getParam($key)); 
                }
            }   


            $model = Mage::getModel('custom/custom');       
            $model-&gt;setData($data)
                -&gt;setId($this-&gt;getRequest()-&gt;getParam('id'));

            try 
            {
                $read = Mage::getSingleton('core/resource')-&gt;getConnection('core_read');
                $write = Mage::getSingleton('core/resource')-&gt;getConnection('core_write');
                //$data = $this-&gt;getRequest()-&gt;getPost();   
                $blockid=$this-&gt;getRequest()-&gt;getParam('id');
                if(!isset($blockid) || $blockid=='') // check if it is a new block
                {
                    if($data['sort']=='') //check if it contains 'sort' value
                    {
                        $resultArray1 = $read-&gt;fetchAll("select * from custom where page_id ='".$data['page_id']."'");
                        $totalRow=count($resultArray1);
                        $data['sort']=$resultArray1[$totalRow-1]['sort'];
                        $data['sort']=$data['sort']+1;
                        Mage::log('ashu11'.$data['sort']);
                    }
                    else
                    {
                        $resultArray2 = $read-&gt;fetchAll("select * from custom where page_id ='".$data['page_id']."' and sort&gt;='".$data['sort']."'");
                        if(count($resultArray2)&gt;0)
                        {
                            foreach($resultArray2 as $result)
                            {
                                $write-&gt;query("update custom set sort ='".++$data['sort']."' where id='".$result['id']."'"); 
                            }
                        }
                    }
                }
                else
                {
                    if($data['sort']=='') //check if it contains 'sort' value
                    {
                        $resultArray3 = $read-&gt;fetchAll("select * from custom where page_id ='".$data['page_id']."' AND id='".$blockid."'");
                        $totalRow=count($resultArray3);
                        $data['sort']=$resultArray3[0]['sort'];
                    }
                    else
                    {
                        $resultArray4 = $read-&gt;fetchAll("select * from custom where page_id ='".$data['page_id']."' AND id='".$blockid."'");
                        $sort1=$resultArray4[0]['sort'];
                        $sort2=$data['sort'];
                        if($sort2&gt;$sort1)//downwoards
                        {
                            $resultArray5 = $read-&gt;fetchAll("select * from custom where page_id ='".$data['page_id']."' AND sort &gt;'".$sort1."' AND sort&lt;='".$sort2."'");
                            foreach($resultArray5 as $result)
                            {
                                $write-&gt;query("update custom set sort ='".--$result['sort']."' where id='".$result['id']."'"); 
                            }
                            $write-&gt;query("update custom set sort ='".$sort2."' where id='".$blockid."'"); 
                        }
                        else
                        {

                            $resultArray7 = $read-&gt;fetchAll("select * from custom where page_id ='".$data['page_id']."' AND sort&lt;'".$sort1."' AND sort&gt;='".$sort2."'");
                            foreach($resultArray7 as $result)
                            {
                                Mage::log($result['id']);
                                $write-&gt;query("update custom set sort ='".++$result['sort']."' where id='".$result['id']."'"); 
                            }
                            $resultArray6 = $read-&gt;fetchAll("select * from custom where page_id ='".$data['page_id']."' AND sort='".$sort2."'");
                            $write-&gt;query("update custom set sort ='".$sort1."' where id='".$blockid."'"); 
                        }
                    }

                }

                $model-&gt;setData($data)
                -&gt;setId($this-&gt;getRequest()-&gt;getParam('id'));
                $model-&gt;save();

                Mage::getSingleton('adminhtml/session')-&gt;addSuccess(Mage::helper('custom')-&gt;__('Block was successfully saved'));
                Mage::getSingleton('adminhtml/session')-&gt;setFormData(false);

                if ($this-&gt;getRequest()-&gt;getParam('back')) {
                    $this-&gt;_redirect('*/*/edit', array('page_id' =&gt; $this-&gt;getRequest()-&gt;getParam('page_id'),'id' =&gt; $model-&gt;getId()));
                    return;
                }
                $this-&gt;_redirect('adminhtml/cms_page/index/');
                return;
            } catch (Exception $e) {
                Mage::getSingleton('adminhtml/session')-&gt;addError($e-&gt;getMessage());
                Mage::getSingleton('adminhtml/session')-&gt;setFormData($data);
                $this-&gt;_redirect('*/*/edit', array('page_id' =&gt; $this-&gt;getRequest()-&gt;getParam('page_id'),'id' =&gt; $this-&gt;getRequest()-&gt;getParam('id')));
                return;
            }
        }
        Mage::getSingleton('adminhtml/session')-&gt;addError(Mage::helper('custom')-&gt;__('Unable to find block to save'));
        $this-&gt;_redirect('adminhtml/cms_page/index/');
    }

    public function deleteAction()
    {
        if( $this-&gt;getRequest()-&gt;getParam('id') &gt; 0 &amp;&amp; $this-&gt;getRequest()-&gt;getParam('page_id')) {
            try {


                $read = Mage::getSingleton('core/resource')-&gt;getConnection('core_read');
                $write = Mage::getSingleton('core/resource')-&gt;getConnection('core_write');
                $sortTobeDelete=$read-&gt;fetchOne("select sort from custom where id='".$this-&gt;getRequest()-&gt;getParam('id')."'");
                Mage::log($sortTobeDelete);

                $resultArray = $read-&gt;fetchAll("select * from custom where page_id ='".$this-&gt;getRequest()-&gt;getParam('page_id')."' and sort &gt;'".$sortTobeDelete."'");
                Mage::log($resultArray);
                if(count($resultArray)&gt;0)
                {
                    foreach($resultArray as $result)
                    {
                        $write-&gt;query("update custom set sort ='".--$result['sort']."' where id='".$result['id']."'"); 
                    }
                }


                $model = Mage::getModel('custom/custom');

                $model-&gt;setId($this-&gt;getRequest()-&gt;getParam('id'))
                    -&gt;delete();

                Mage::getSingleton('adminhtml/session')-&gt;addSuccess(Mage::helper('adminhtml')-&gt;__('Item was successfully deleted'));
                $this-&gt;_redirect('adminhtml/cms_page/index/');
            } catch (Exception $e) {
                Mage::getSingleton('adminhtml/session')-&gt;addError($e-&gt;getMessage());
                $this-&gt;_redirect('*/*/edit', array('page_id' =&gt; $this-&gt;getRequest()-&gt;getParam('page_id'),'id' =&gt; $this-&gt;getRequest()-&gt;getParam('id')));
            }
        }
        $this-&gt;_redirect('adminhtml/cms_page/index/');
    }

    public function sortRowAction() {
        $currentIndex=$this-&gt;getRequest()-&gt;getPost('curId');
        $changedIndex=$this-&gt;getRequest()-&gt;getPost('chaId');
        $rowId=$this-&gt;getRequest()-&gt;getPost('rId');
        $pageId=$this-&gt;getRequest()-&gt;getPost('pageId');


        $output['currentIndex'] = $currentIndex;
        $output['changedIndex'] = $changedIndex;
        $output['rowId'] = $rowId;
        $output['pageId'] = $pageId;
        $output['ashu'] = "sdfds";

        $read = Mage::getSingleton('core/resource')-&gt;getConnection('core_read');
        $write = Mage::getSingleton('core/resource')-&gt;getConnection('core_write');

        $sort1=$currentIndex;
        $sort2=$changedIndex;

        try
        {   
            if($sort2&gt;$sort1)//downwoards
            {
                $resultArray5 = $read-&gt;fetchAll("select * from custom where page_id ='".$pageId."' AND sort &gt;'".$sort1."' AND sort&lt;='".$sort2."'");
                foreach($resultArray5 as $result)
                {
                    $write-&gt;query("update custom set sort ='".--$result['sort']."' where id='".$result['id']."'"); 
                }
                $write-&gt;query("update custom set sort ='".$sort2."' where id='".$rowId."'"); 
            }
            else
            {

                $resultArray7 = $read-&gt;fetchAll("select * from custom where page_id ='".$pageId."' AND sort&lt;'".$sort1."' AND sort&gt;='".$sort2."'");
                foreach($resultArray7 as $result)
                {
                    $write-&gt;query("update custom set sort ='".++$result['sort']."' where id='".$result['id']."'"); 
                }
                $write-&gt;query("update custom set sort ='".$sort2."' where id='".$rowId."'"); 
            }

        }catch (Exception $e) {
                Mage::getSingleton('adminhtml/session')-&gt;addError($e-&gt;getMessage());
                Mage::getSingleton('adminhtml/session')-&gt;setFormData($data);
                return;
          }

        $json = json_encode($output);
        $this-&gt;getResponse()
                             -&gt;clearHeaders()
                             -&gt;setHeader('Content-Type', 'application/json')
                             -&gt;setBody($json);
    }

    public function removeFile($file) {
        $_helper = Mage::helper('custom');
        $file = $_helper-&gt;updateDirSepereator($file);
        $directory = Mage::getBaseDir('media') . DS . $file;
        $io = new Varien_Io_File();
        $result = $io-&gt;rmdir($directory, true);
    }

}
</code></pre>

<p>This code is running well on my localhost even on another server. but can't find out why it is nor working on its actual server.</p>

<p><strong>.htacess</strong>--</p>

<pre><code>############################################
## uncomment these lines for CGI mode
## make sure to specify the correct cgi php binary file name
## it might be /cgi-bin/php-cgi

#    Action php5-cgi /cgi-bin/php5-cgi
#    AddHandler php5-cgi .php

############################################
## GoDaddy specific options

#   Options -MultiViews

## you might also need to add this line to php.ini
##     cgi.fix_pathinfo = 1
## if it still doesn't work, rename php.ini to php5.ini

############################################
## this line is specific for 1and1 hosting

    #AddType x-mapp-php5 .php
    #AddHandler x-mapp-php5 .php

############################################
## default index file

    DirectoryIndex index.php

&lt;IfModule mod_php5.c&gt;

############################################
## adjust memory limit

#    php_value memory_limit 64M
    php_value memory_limit 256M
    php_value max_execution_time 18000

############################################
## disable magic quotes for php request vars

    php_flag magic_quotes_gpc off

############################################
## disable automatic session start
## before autoload was initialized

    php_flag session.auto_start off

############################################
## enable resulting html compression

    #php_flag zlib.output_compression on

###########################################
# disable user agent verification to not break multiple image upload

    php_flag suhosin.session.cryptua off

###########################################
# turn off compatibility with PHP4 when dealing with objects

    php_flag zend.ze1_compatibility_mode Off

&lt;/IfModule&gt;

&lt;IfModule mod_security.c&gt;
###########################################
# disable POST processing to not break multiple image upload

    SecFilterEngine Off
    SecFilterScanPOST Off
&lt;/IfModule&gt;

&lt;IfModule mod_deflate.c&gt;

############################################
## enable apache served files compression
## http://developer.yahoo.com/performance/rules.html#gzip

    # Insert filter on all content
    ###SetOutputFilter DEFLATE
    # Insert filter on selected content types only
    #AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript

    # Netscape 4.x has some problems...
    #BrowserMatch ^Mozilla/4 gzip-only-text/html

    # Netscape 4.06-4.08 have some more problems
    #BrowserMatch ^Mozilla/4\.0[678] no-gzip

    # MSIE masquerades as Netscape, but it is fine
    #BrowserMatch \bMSIE !no-gzip !gzip-only-text/html

    # Don't compress images
    #SetEnvIfNoCase Request_URI \.(?:gif|jpe?g|png)$ no-gzip dont-vary

    # Make sure proxies don't deliver the wrong content
    #Header append Vary User-Agent env=!dont-vary

&lt;/IfModule&gt;

&lt;IfModule mod_ssl.c&gt;

############################################
## make HTTPS env vars available for CGI mode

    SSLOptions StdEnvVars

&lt;/IfModule&gt;

&lt;IfModule mod_rewrite.c&gt;

############################################
## enable rewrites

    Options +FollowSymLinks
    RewriteEngine on

############################################
## you can put here your magento root folder
## path relative to web root

    #RewriteBase /magento/

############################################
## uncomment next line to enable light API calls processing

#    RewriteRule ^api/([a-z][0-9a-z_]+)/?$ api.php?type=$1 [QSA,L]

############################################
## rewrite API2 calls to api.php (by now it is REST only)

    RewriteRule ^api/rest api.php?type=rest [QSA,L]

############################################
## workaround for HTTP authorization
## in CGI environment

    RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]

############################################
## TRACE and TRACK HTTP methods disabled to prevent XSS attacks

    RewriteCond %{REQUEST_METHOD} ^TRAC[EK]
    RewriteRule .* - [L,R=405]

############################################
## redirect for mobile user agents

    #RewriteCond %{REQUEST_URI} !^/mobiledirectoryhere/.*$
    #RewriteCond %{HTTP_USER_AGENT} "android|blackberry|ipad|iphone|ipod|iemobile|opera mobile|palmos|webos|googlebot-mobile" [NC]
    #RewriteRule ^(.*)$ /mobiledirectoryhere/ [L,R=302]

############################################
## always send 404 on missing files in these folders

   RewriteCond %{REQUEST_URI} !^/(media|skin|js)/

############################################
## never rewrite for existing files, directories and links

    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteCond %{REQUEST_FILENAME} !-l

############################################
## rewrite everything else to index.php

    RewriteRule .* index.php [L]

&lt;/IfModule&gt;


############################################
## Prevent character encoding issues from server overrides
## If you still have problems, use the second line instead

    AddDefaultCharset Off
    #AddDefaultCharset UTF-8

&lt;IfModule mod_expires.c&gt;

############################################
## Add default Expires header
## http://developer.yahoo.com/performance/rules.html#expires

    ExpiresDefault "access plus 1 year"

&lt;/IfModule&gt;

############################################
## By default allow all access

    Order allow,deny
    Allow from all

###########################################
## Deny access to release notes to prevent disclosure of the installed Magento version

    &lt;Files RELEASE_NOTES.txt&gt;
        order allow,deny
        deny from all
    &lt;/Files&gt;

############################################
## If running in cluster environment, uncomment this
## http://developer.yahoo.com/performance/rules.html#etags

    #FileETag none
</code></pre>

<p>Can anyone help me pls to find out issue.</p>

